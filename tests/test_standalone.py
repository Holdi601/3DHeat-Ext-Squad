"""The standalone app's own parts, on a synthetic game install (no game files)."""

from __future__ import annotations

import hashlib
import importlib
import io
import json
import os
import re
import tarfile
import time
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / "standalone.json").read_text(encoding="utf-8"))
PKG = CFG["spec"].split(".")[0]
app_entry = importlib.import_module(f"{PKG}.app.entry")
app_update = importlib.import_module(f"{PKG}.app.update")
app_paths = importlib.import_module(f"{PKG}.app.paths")
app_spec = importlib.import_module(f"{PKG}.app.spec")
app_manifest = importlib.import_module(f"{PKG}.app.manifest")


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "appdata"))
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "appdata"))
    monkeypatch.setenv("HEAT3D_LEVELS", str(tmp_path / "levels"))
    monkeypatch.setenv("HEAT3D_NO_UPDATE", "1")
    monkeypatch.delenv("HEAT3D_AUTO_UPDATE", raising=False)
    app_update.AUTO_THIS_RUN = False


def fake_spec(game: Path):
    S = app_spec

    def maps(root: Path):
        return [S.MapSource(p.stem, p.stem.title(), [p]) for p in sorted((root / "maps").glob("*.map"))]

    def extract(root: Path, m, out: Path, log):
        dest = out / m.id / f"{m.id}.glb"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(m.sources[0].read_bytes())
        log(f"ok {dest}")
        return [dest]

    g = S.GameSpec("fake", "Fake Game", lambda given: game if (game / "maps").is_dir() else None,
                   subdir="fake", maps=maps, extract=extract,
                   existing_outputs=lambda out, m: [out / m.id / f"{m.id}.glb"], output_version="1.0.0",
                   build=lambda root: (root / "build.txt").read_text().strip())
    return S.Spec("heat3d-fake", "Fake", "Holdi601/3DHeat-Fake", "1.0.0", tools={}, default_tool="",
                  games=[g], module="x")


def age(path: Path, seconds: float) -> None:
    """Set a file's time `seconds` into the past (outputs older than their game files: outdated)."""
    t = time.time() - seconds
    os.utime(path, (t, t))


def run(spec, *argv, capsys):
    code = app_entry.main(spec, list(argv))
    out = capsys.readouterr().out
    return code, out


def test_real_spec_loads():
    spec = importlib.import_module(CFG["spec"]).SPEC
    assert spec.id.startswith("heat3d-") and spec.repo.startswith("Holdi601/")
    assert spec.version == (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    assert spec.default_tool in spec.tools
    for plat in CFG["platforms"]:
        assert plat in ("windows-x64", "linux-x64", "macos-arm64")


def test_real_spec_cli(capsys):
    spec = importlib.import_module(CFG["spec"]).SPEC
    code, out = run(spec, "--version", capsys=capsys)
    assert code == 0 and out.strip() == f"{spec.id} {spec.version}"
    code, out = run(spec, "--check", "--json", capsys=capsys)
    doc = json.loads(out)
    assert doc["id"] == spec.id and any(c["id"] == "disk" for c in doc["checks"])
    code, out = run(spec, "status", "--json", capsys=capsys)
    doc = json.loads(out)
    assert code == 0 and doc["id"] == spec.id
    assert app_entry.main(spec, ["--gui-selftest"]) == 0


def test_install_that_gains_a_map(tmp_path, capsys):
    game = tmp_path / "game"
    (game / "maps").mkdir(parents=True)
    (game / "build.txt").write_text("100")
    (game / "maps" / "alpha.map").write_bytes(b"a" * 10)
    (game / "maps" / "bravo.map").write_bytes(b"b" * 10)
    spec = fake_spec(game)

    _, out = run(spec, "status", "--json", capsys=capsys)
    g = json.loads(out)["games"][0]
    assert g["found"] and g["build"] == "100" and g["counts"]["new"] == 2

    code, out = run(spec, "extract", "--new", "--progress-json", capsys=capsys)
    events = [json.loads(l) for l in out.splitlines() if l.startswith("{")]
    assert code == 0 and events[0] == {"event": "start", "total": 2} and events[-1]["ok"] == 2
    man = json.loads((tmp_path / "levels" / "fake" / ".heat3d-extract.json").read_text())
    assert set(man["entries"]) == {"alpha", "bravo"}
    e = man["entries"]["alpha"]
    assert e["extractor_version"] == "1.0.0" and e["game_build"] == "100"
    assert e["sources"]["maps/alpha.map"]["sha256"] == hashlib.sha256(b"a" * 10).hexdigest()
    assert e["outputs"] == ["fake/alpha/alpha.glb"]

    # A DLC adds a map, a game update changes one, another is only touched.
    (game / "maps" / "charlie.map").write_bytes(b"c" * 10)
    (game / "maps" / "bravo.map").write_bytes(b"B" * 12)
    t = time.time() + 5
    os.utime(game / "maps" / "alpha.map", (t, t))
    _, out = run(spec, "status", "--json", capsys=capsys)
    states = {m["id"]: m["state"] for m in json.loads(out)["games"][0]["maps"]}
    assert states == {"alpha": "current", "bravo": "changed", "charlie": "new"}

    # Only the new one, then only the changed one: the rest is not redone.
    before = (tmp_path / "levels" / "fake" / "alpha" / "alpha.glb").stat().st_mtime_ns
    code, out = run(spec, "extract", "charlie", "--progress-json", capsys=capsys)
    assert [json.loads(l)["id"] for l in out.splitlines() if '"map"' in l] == ["charlie"]
    code, out = run(spec, "extract", "--changed", "--progress-json", capsys=capsys)
    assert [json.loads(l)["id"] for l in out.splitlines() if '"map"' in l] == ["bravo"]
    assert (tmp_path / "levels" / "fake" / "alpha" / "alpha.glb").stat().st_mtime_ns == before
    _, out = run(spec, "status", "--json", capsys=capsys)
    assert json.loads(out)["games"][0]["counts"]["current"] == 3

    # A newer extractor whose output changed makes the old extracts outdated; a map that left is reported.
    spec.games[0].output_version = "2.0.0"
    (game / "maps" / "alpha.map").unlink()
    _, out = run(spec, "status", "--json", capsys=capsys)
    c = json.loads(out)["games"][0]["counts"]
    assert c["outdated"] == 2 and c["missing"] == 1


def test_untracked_extract_counts_as_outdated(tmp_path, capsys):
    game = tmp_path / "game"
    (game / "maps").mkdir(parents=True)
    (game / "build.txt").write_text("1")
    (game / "maps" / "alpha.map").write_bytes(b"a")
    out = tmp_path / "levels" / "fake" / "alpha"
    out.mkdir(parents=True)
    (out / "alpha.glb").write_bytes(b"old")
    age(out / "alpha.glb", 3600)  # older than the game file it was made from
    _, text = run(fake_spec(game), "status", "--json", capsys=capsys)
    assert json.loads(text)["games"][0]["maps"][0]["state"] == "outdated"
    assert "untracked" not in json.loads(text)["games"][0]["maps"][0]


def test_untracked_extract_newer_than_its_sources_counts_as_current(tmp_path, capsys, quiet):
    game = make_game(tmp_path, maps=("alpha", "bravo"))
    out = tmp_path / "levels" / "fake"
    for m in ("alpha", "bravo"):
        age(game / "maps" / f"{m}.map", 7200)
        (out / m).mkdir(parents=True)
        (out / m / f"{m}.glb").write_bytes(b"old")
    age(out / "bravo" / "bravo.glb", 9000)  # older than bravo.map: outdated
    spec = fake_spec(game)
    _, text = run(spec, "status", "--json", capsys=capsys)
    g = json.loads(text)["games"][0]
    by = {m["id"]: m for m in g["maps"]}
    assert by["alpha"] == {"id": "alpha", "title": "Alpha", "state": "current", "extracted_version": None,
                           "untracked": True}
    assert by["bravo"]["state"] == "outdated" and "untracked" not in by["bravo"]
    assert g["counts"]["current"] == 1 and g["counts"]["outdated"] == 1
    assert not (out / app_manifest.NAME).exists()  # not recorded
    # neither extract --outdated nor the unattended check replaces an untracked current output
    run(spec, "extract", "--outdated", capsys=capsys)
    assert (out / "alpha" / "alpha.glb").read_bytes() == b"old" and (out / "bravo" / "bravo.glb").read_bytes() == b"bravo" * 4
    (out / "alpha" / "alpha.glb").write_bytes(b"old")
    _, text = run(spec, "check-new", "--json", "--auto-extract", capsys=capsys)
    assert json.loads(text)["games"][0]["auto_extracted"] == []
    assert (out / "alpha" / "alpha.glb").read_bytes() == b"old"


def test_adopt_hook_decides_untracked_entries(tmp_path, capsys, quiet):
    game = make_game(tmp_path, maps=("alpha", "bravo", "charlie", "delta"))
    out = tmp_path / "levels" / "fake"
    for m in ("alpha", "bravo", "charlie", "delta"):
        (out / m).mkdir(parents=True)
        (out / m / f"{m}.glb").write_bytes(b"old")
        age(out / m / f"{m}.glb", 3600)  # by the times alone all four would be outdated
    (out / "catalog.json").write_text(json.dumps({"items": []}))
    answers = {"alpha": ("1.0.0", "current"), "bravo": ("0.5.0", "current"), "charlie": ("1.0.0", "changed"),
               "delta": None, "catalog": ("1.2.0", "current")}
    asked = []

    def adopt(root, m, o):
        asked.append(m.id)
        assert root == game and o == out
        if m.id == "delta":
            raise RuntimeError("cannot tell")  # an answer that breaks counts as no answer
        return answers[m.id]

    spec = content_spec(game)
    spec.games[0].adopt = adopt
    _, text = run(spec, "status", "--json", capsys=capsys)
    g = json.loads(text)["games"][0]
    by = {m["id"]: (m["state"], m["extracted_version"]) for m in g["maps"]}
    assert by == {"alpha": ("current", "1.0.0"), "bravo": ("outdated", "0.5.0"), "charlie": ("changed", "1.0.0"),
                  "delta": ("outdated", None)}
    assert g["content"][0]["state"] == "current" and g["content"][0]["extracted_version"] == "1.2.0"
    assert all("untracked" not in m for m in g["maps"])
    entries = json.loads((out / app_manifest.NAME).read_text(encoding="utf-8"))["entries"]
    assert sorted(entries) == ["alpha", "bravo", "content:catalog"]  # "changed" and unknown: not recorded
    assert entries["alpha"]["extractor_version"] == "1.0.0" and entries["alpha"]["game_build"] == "100"
    assert list(entries["alpha"]["sources"]) == ["maps/alpha.map"]
    assert entries["alpha"]["outputs"] == ["fake/alpha/alpha.glb"] and entries["content:catalog"]["kind"] == "catalog"
    # adopted entries come from the manifest from now on; the hook is asked only for untracked ones
    asked.clear()
    _, text = run(spec, "status", "--json", capsys=capsys)
    assert sorted(asked) == ["charlie", "delta"]
    by = {m["id"]: m["state"] for m in json.loads(text)["games"][0]["maps"]}
    assert by == {"alpha": "current", "bravo": "outdated", "charlie": "changed", "delta": "outdated"}
    # a game file changed after the adopt is noticed like after any extract
    (game / "maps" / "alpha.map").write_bytes(b"patched")
    _, text = run(spec, "status", "--json", capsys=capsys)
    assert {m["id"]: m["state"] for m in json.loads(text)["games"][0]["maps"]}["alpha"] == "changed"


def test_source_rewritten_within_the_same_tick_is_still_changed(tmp_path, capsys):
    game = make_game(tmp_path, maps=("alpha",))
    spec = fake_spec(game)
    run(spec, "extract", "alpha", capsys=capsys)
    src = game / "maps" / "alpha.map"
    st = src.stat()
    src.write_bytes(b"z" * st.st_size)  # same size, and the same time as recorded (a coarse clock)
    os.utime(src, ns=(st.st_atime_ns, st.st_mtime_ns))
    _, text = run(spec, "status", "--json", capsys=capsys)
    assert json.loads(text)["games"][0]["maps"][0]["state"] == "changed"


def test_game_not_found(tmp_path, capsys):
    spec = fake_spec(tmp_path / "nowhere")
    _, out = run(spec, "--check", "--json", capsys=capsys)
    checks = {c["id"]: c for c in json.loads(out)["checks"]}
    assert checks["game:fake"]["ok"] is False
    code, out = run(spec, "extract", "--new", "--progress-json", capsys=capsys)
    assert code == 0 and json.loads(out.splitlines()[-1]) == {"event": "done", "ok": 0, "failed": 0}


def test_versions():
    U = app_update
    assert U.is_newer("v1.10.0", "1.9.9") and not U.is_newer("1.0", "1.0.0")
    assert not U.is_newer("1.0.0-rc1", "1.0.0") and U.is_newer("2", "1.99.99")
    assert app_manifest.older("0.9", "1.0.0") and not app_manifest.older("1.0.0", "1.0")


def test_checksums():
    U = app_update
    blob = b"standalone"
    h = hashlib.sha256(blob).hexdigest()
    sums = U.parse_sums(f"{h}  x.zip\n{'0' * 64}  y.tar.gz\n")
    assert U.verify(blob, "x.zip", sums, f"sha256:{h}") == h
    with pytest.raises(RuntimeError):
        U.verify(blob, "y.tar.gz", sums)
    with pytest.raises(RuntimeError):
        U.verify(blob, "x.zip", sums, "sha256:" + "1" * 64)
    with pytest.raises(RuntimeError):
        U.verify(blob, "z.zip", sums)


def test_unpack_refuses_escapes(tmp_path):
    U = app_update
    good = io.BytesIO()
    with zipfile.ZipFile(good, "w") as z:
        z.writestr("tool/tool.exe", b"x")
    assert (U.unpack(good.getvalue(), "a.zip", tmp_path / "g", "tool") / "tool.exe").is_file()
    for bad in ("../evil", "other/x", "/abs", "tool/../../evil"):
        b = io.BytesIO()
        with zipfile.ZipFile(b, "w") as z:
            z.writestr(bad, b"x")
        with pytest.raises(RuntimeError):
            U.unpack(b.getvalue(), "a.zip", tmp_path / "b", "tool")
    t = io.BytesIO()
    with tarfile.open(fileobj=t, mode="w:gz") as tf:
        info = tarfile.TarInfo("tool/link")
        info.type = tarfile.SYMTYPE
        info.linkname = "/etc/passwd"
        tf.addfile(info)
    with pytest.raises(RuntimeError):
        U.unpack(t.getvalue(), "a.tar.gz", tmp_path / "t", "tool")


def test_update_asks_unless_auto(tmp_path, monkeypatch, capsys):
    U = app_update
    t = U.Target("Holdi601/3DHeat-Fake", "heat3d-fake", "Fake", "1.0.0", apply_source=lambda r: "applied")
    r = U.Release("1.1.0", "v1.1.0", "- better maps", "https://github.com/x")
    monkeypatch.delenv("HEAT3D_NO_UPDATE")
    monkeypatch.setattr(U, "latest", lambda target, use_cache=True: r)
    applied = []
    monkeypatch.setattr(U, "_apply_and_restart", lambda target, release: applied.append(release.version))
    U.startup(t, ask=False)  # nobody to ask: announced only
    assert applied == [] and "1.1.0" in capsys.readouterr().err
    monkeypatch.setattr("builtins.input", lambda *_: "s")
    U.startup(t, ask=True)  # skipped: not announced again
    assert U.available(t) is None and U.available(t, include_skipped=True) is r
    U.set_auto("heat3d-fake", True)
    monkeypatch.setattr(U, "latest", lambda target, use_cache=True: U.Release("1.2.0", "v1.2.0", "", ""))
    U.startup(t, ask=False)
    assert applied == ["1.2.0"]


def test_steam_libraries(tmp_path):
    P = app_paths
    root = tmp_path / "Steam"
    lib2 = tmp_path / "Library2"
    for lib in (root, lib2):
        (lib / "steamapps" / "common" / "Some Game").mkdir(parents=True)
    (root / "steamapps" / "libraryfolders.vdf").write_text(
        '"libraryfolders"\n{\n "0" { "path" "%s" }\n "1" { "path" "%s" }\n}\n'
        % (str(root).replace("\\", "\\\\"), str(lib2).replace("\\", "\\\\")))
    libs = P.steam_libraries([root])
    assert [p.resolve() for p in libs] == [root.resolve(), lib2.resolve()]
    assert len(P.steam_game_dirs("Some Game", libs)) == 2
    (lib2 / "steamapps" / "appmanifest_4242.acf").write_text('"AppState"\n{\n "appid" "4242"\n "installdir" "Some Game"\n}\n')
    pfx = lib2 / "steamapps" / "compatdata" / "4242" / "pfx" / "drive_c" / "users" / "steamuser" / "Documents"
    pfx.mkdir(parents=True)
    game = lib2 / "steamapps" / "common" / "Some Game"
    assert P.steam_app_id(lib2, "Some Game") == "4242"
    assert P.proton_user_dir(game, "Documents") == pfx


def test_replay_contract(tmp_path, capsys, monkeypatch):
    """`convert <replay> -o <out> [--progress-json]` and `info <replay> --json`, for any replay reader."""
    S = app_spec
    seen = []

    def tool(argv):
        seen.append(argv)
        src, out = Path(argv[0]), Path(argv[2])
        if src.read_bytes() == b"bad":
            raise ValueError("not a replay")
        (out / (src.stem + ".3dheat")).write_bytes(b"x")
        print("1/1 written")
        return 0

    mod = type(__import__("sys"))("fake_reader")
    mod.main = tool
    monkeypatch.setitem(__import__("sys").modules, "fake_reader", mod)
    reader = S.Replays("fake", (".rep",), lambda r, out: ["fake-replay", str(r), "-o", str(out)],
                       info=lambda p: {"map": "alpha", "players": [{"name": "A", "team": 1}]})
    spec = S.Spec("heat3d-fake", "Fake", "Holdi601/3DHeat-Fake", "1.0.0", tools={"fake-replay": "fake_reader:main"},
                  default_tool="fake-replay", module="x", replays=reader)
    good, bad = tmp_path / "a.rep", tmp_path / "b.rep"
    good.write_bytes(b"ok")
    bad.write_bytes(b"bad")
    out = tmp_path / "out"
    code, text = run(spec, "convert", str(good), str(bad), "-o", str(out), "--progress-json", capsys=capsys)
    lines = [json.loads(l) for l in text.splitlines()]  # stdout holds JSON lines only
    assert code == 1 and (out / "a.3dheat").is_file()
    assert lines[0] == {"event": "start", "total": 2} and lines[-1] == {"event": "done", "ok": 1, "failed": 1}
    assert [l["state"] for l in lines if l.get("event") == "file"] == ["ok", "failed"]
    code, text = run(spec, "info", str(good), "--json", capsys=capsys)
    doc = json.loads(text)
    assert code == 0 and doc["game"] == "fake" and doc["map"] == "alpha" and doc["complete"] is True
    assert doc["converter"] == {"id": "heat3d-fake", "version": "1.0.0"} and doc["mode"] is None and doc["date"]
    reader.info = lambda p: (_ for _ in ()).throw(ValueError("not a replay"))
    code, text = run(spec, "info", str(bad), "--json", capsys=capsys)
    assert code == 1 and "not a replay" in json.loads(text)["error"]


def test_real_spec_replay_verbs(capsys):
    spec = importlib.import_module(CFG["spec"]).SPEC
    if spec.replays is None:
        pytest.skip("not a replay reader")
    assert spec.replays.extensions and all(e.startswith(".") for e in spec.replays.extensions)
    assert spec.replays.convert(Path("r" + spec.replays.extensions[0]), Path("out"))[0] in spec.tools
    with pytest.raises(SystemExit) as e:
        app_entry.main(spec, ["convert", "--help"])
    assert e.value.code == 0


def test_tray_says_what_it_does(monkeypatch):
    tray = importlib.import_module(f"{PKG}.app.tray")
    s = tray.TrayState("3DHeat Watcher")
    assert s.status() == "Not recording" and [a for _, a in s.menu()] == [None, None, "open", "quit"]
    s.state, s.what, s.since = "recording", "Watch my games", 1000.0
    assert s.status(now=1000.0 + 75 * 60) == "Recording: Watch my games (1 h 15 min)"
    assert "pause" in [a for _, a in s.menu()] and "resume" not in [a for _, a in s.menu()]
    s.state = "paused"
    assert s.status() == "Paused: Watch my games" and "resume" in [a for _, a in s.menu()]
    s.what = "x" * 300
    assert len(s.tooltip()) == 127
    # No icon where there is none to have: the window then behaves as before.
    monkeypatch.setenv("HEAT3D_NO_TRAY", "1")
    assert tray.start("3DHeat Watcher", lambda a: None) is None


# ------------------------------------------------------------------ new content: catalogue, items, check-new

app_guard = importlib.import_module(f"{PKG}.app.guard")
app_tray = importlib.import_module(f"{PKG}.app.tray")


def content_spec(game: Path):
    """fake_spec plus a catalogue: made from catalog/items.txt ("kind:id" lines), written as <out>/catalog.json."""
    S = app_spec
    spec = fake_spec(game)
    g = spec.games[0]

    def items(root: Path) -> dict:
        got: dict = {}
        for line in (root / "catalog" / "items.txt").read_text().split():
            kind, _, iid = line.partition(":")
            got.setdefault(kind, []).append(iid)
        return got

    def extract_content(root: Path, c, out: Path, log):
        dest = out / "catalog.json"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps({"items": [{"id": i, "kind": k} for k, v in items(root).items() for i in v]}))
        return [dest]

    g.contents = lambda root: [S.MapSource("catalog", "Vehicles and weapons", [root / "catalog" / "items.txt"],
                                           kind="catalog")]
    g.extract_content = extract_content
    g.catalog_items = items
    return spec


def make_game(tmp_path: Path, maps=("alpha", "bravo"), items=("vehicle:t1", "vehicle:t2", "weapon:w1")) -> Path:
    game = tmp_path / "game"
    (game / "maps").mkdir(parents=True)
    (game / "catalog").mkdir()
    (game / "build.txt").write_text("100")
    for m in maps:
        (game / "maps" / f"{m}.map").write_bytes(m.encode() * 4)
    (game / "catalog" / "items.txt").write_text("\n".join(items))
    return game


@pytest.fixture
def quiet(monkeypatch):
    """check-new without the real process scan, store check and priority change (each tested on its own)."""
    calls = []
    monkeypatch.setattr(app_guard, "lower_priority", lambda: calls.append("lowered"))
    monkeypatch.setattr(app_guard, "game_running", lambda install, exes=None: False)
    monkeypatch.setattr(app_guard, "game_updating", lambda install, now=None: False)
    return calls


def test_status_without_content_hooks_only_adds_empty_fields(tmp_path, capsys):
    game = make_game(tmp_path)
    _, out = run(fake_spec(game), "status", "--json", capsys=capsys)
    g = json.loads(out)["games"][0]
    assert g["content"] == [] and set(g["content_counts"].values()) == {0} and g["build_changed"] is False
    assert g["items"] == {"install": {}, "extracted": {}, "new": {}, "new_count": 0, "gone_count": 0}
    assert set(g["maps"][0]) == {"id", "title", "state", "extracted_version"} and g["counts"]["new"] == 2


def test_content_states_and_items(tmp_path, capsys):
    game = make_game(tmp_path)
    spec = content_spec(game)
    _, out = run(spec, "status", "--json", capsys=capsys)
    g = json.loads(out)["games"][0]
    assert g["content"] == [{"id": "catalog", "kind": "catalog", "title": "Vehicles and weapons", "state": "new",
                             "extracted_version": None}]
    assert g["content_counts"]["new"] == 1
    assert g["items"]["install"] == {"vehicle": 2, "weapon": 1} and g["items"]["new_count"] == 3

    # --new alone: maps only (old callers unchanged)
    code, out = run(spec, "extract", "--new", "--progress-json", capsys=capsys)
    assert [json.loads(l)["id"] for l in out.splitlines() if '"map"' in l] == ["alpha", "bravo"]
    code, out = run(spec, "extract", "--new", "--content", "--progress-json", capsys=capsys)
    assert code == 0 and [json.loads(l)["id"] for l in out.splitlines() if '"map"' in l] == ["content:catalog"]
    man = json.loads((tmp_path / "levels" / "fake" / ".heat3d-extract.json").read_text())
    assert man["entries"]["content:catalog"]["kind"] == "catalog"
    _, out = run(spec, "status", "--json", capsys=capsys)
    g = json.loads(out)["games"][0]
    assert g["content"][0]["state"] == "current" and g["items"]["new_count"] == 0
    assert g["items"]["extracted"] == {"vehicle": 2, "weapon": 1}

    # A game update adds a vehicle and drops a weapon; then a new build.
    (game / "catalog" / "items.txt").write_text("vehicle:t1\nvehicle:t2\nvehicle:t3")
    (game / "build.txt").write_text("101")
    _, out = run(spec, "status", "--json", capsys=capsys)
    g = json.loads(out)["games"][0]
    assert g["content"][0]["state"] == "changed" and g["build_changed"] is True
    assert g["items"]["new"] == {"vehicle": ["t3"]} and g["items"]["new_count"] == 1 and g["items"]["gone_count"] == 1
    code, out = run(spec, "extract", "content:catalog", "--progress-json", capsys=capsys)
    assert [json.loads(l)["id"] for l in out.splitlines() if '"map"' in l] == ["content:catalog"]
    _, out = run(spec, "status", "--json", capsys=capsys)
    g = json.loads(out)["games"][0]
    assert g["content_counts"]["current"] == 1 and g["items"]["new_count"] == 0

    # The content entry leaves the install: reported as missing, never a map.
    spec.games[0].contents = lambda root: []
    _, out = run(spec, "status", "--json", capsys=capsys)
    g = json.loads(out)["games"][0]
    assert g["content"] == [{"id": "catalog", "kind": "catalog", "title": "catalog", "state": "missing",
                             "extracted_version": "1.0.0"}]
    assert g["counts"]["missing"] == 0


def test_untracked_catalog_counts_as_outdated(tmp_path, capsys):
    game = make_game(tmp_path)
    out = tmp_path / "levels" / "fake"
    out.mkdir(parents=True)
    (out / "catalog.json").write_text(json.dumps({"items": [{"id": "t1", "category": "vehicle"}]}))
    age(out / "catalog.json", 3600)
    _, text = run(content_spec(game), "status", "--json", capsys=capsys)
    g = json.loads(text)["games"][0]
    assert g["content"][0]["state"] == "outdated"
    assert g["items"]["extracted"] == {"vehicle": 1} and g["items"]["new"] == {"vehicle": ["t2"], "weapon": ["w1"]}


def test_item_diff_caps_ids_not_counts():
    d = app_manifest.item_diff({"vehicle": [f"v{i:03d}" for i in range(120)], "ship": ["s1"]},
                               {"vehicle": [f"v{i:03d}" for i in range(10)] + ["old1", "old2", "old3"]})
    assert d["new_count"] == 111 and d["gone_count"] == 3
    assert len(d["new"]["vehicle"]) == app_manifest.ITEM_IDS == 50 and d["new"]["ship"] == ["s1"]
    assert d["install"] == {"ship": 1, "vehicle": 120} and d["extracted"] == {"vehicle": 13}


def test_check_new_status_file(tmp_path, capsys, quiet):
    game = make_game(tmp_path)
    spec = content_spec(game)
    code, out = run(spec, "check-new", "--json", capsys=capsys)
    doc = json.loads(out)
    assert code == 0 and quiet == ["lowered"]
    f = tmp_path / "levels" / ".heat3d-status" / "heat3d-fake.json"
    assert json.loads(f.read_text()) == doc and not list(f.parent.glob("*.tmp"))
    assert {k: doc[k] for k in ("format", "version", "tool", "toolVersion")} == \
        {"format": "3dheat-content-status", "version": 1, "tool": "heat3d-fake", "toolVersion": "1.0.0"}
    assert re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", doc["at"])
    g = doc["games"][0]
    for k in ("game", "label", "found", "build", "build_changed", "skipped", "counts", "content_counts", "items",
              "new_maps", "replace_maps", "auto_extracted", "failed"):
        assert k in g, k
    assert g["skipped"] is None and g["build"] == "100" and g["new_maps"] == ["alpha", "bravo"]
    assert g["new_content"] == ["content:catalog"] and g["items"]["new_count"] == 3 and g["auto_extracted"] == []
    assert not (tmp_path / "levels" / "fake" / "alpha").exists()  # a check alone writes no maps

    # --game: the other games' entries in the file are kept
    other = app_spec.GameSpec("other", "Other Game", lambda given: None)
    spec.games.append(other)
    run(spec, "check-new", "--game", "other", capsys=capsys)
    games = json.loads(f.read_text())["games"]
    assert [x["game"] for x in games] == ["fake", "other"] and games[0]["new_maps"] == ["alpha", "bravo"]
    assert games[1]["found"] is False


def test_check_new_auto_extract_is_additive_only(tmp_path, capsys, quiet):
    game = make_game(tmp_path, maps=("alpha",))
    spec = content_spec(game)
    run(spec, "extract", "alpha", capsys=capsys)
    # Same size as before; the time is set explicitly, so a coarse file clock cannot hide the update.
    alpha_src = game / "maps" / "alpha.map"
    alpha_src.write_bytes(b"changed by an update")
    age(alpha_src, -10)
    (game / "maps" / "bravo.map").write_bytes(b"b")
    (game / "maps" / "charlie.map").write_bytes(b"c")
    old = tmp_path / "levels" / "fake" / "bravo" / "bravo.glb"  # extracted before manifests, older: outdated
    old.parent.mkdir(parents=True)
    old.write_bytes(b"old")
    age(old, 3600)
    alpha = tmp_path / "levels" / "fake" / "alpha" / "alpha.glb"
    before = alpha.read_bytes()
    code, out = run(spec, "check-new", "--json", "--auto-extract", capsys=capsys)
    g = json.loads(out)["games"][0]
    assert code == 0 and sorted(g["auto_extracted"]) == ["charlie", "content:catalog"] and g["failed"] == []
    assert g["new_maps"] == [] and sorted(g["replace_maps"]) == ["alpha", "bravo"]
    assert alpha.read_bytes() == before and old.read_bytes() == b"old"
    assert (tmp_path / "levels" / "fake" / "charlie" / "charlie.glb").is_file()
    assert g["items"]["new_count"] == 0 and g["auto_extracted_items"]["new_count"] == 3
    assert app_tray.new_content_text(json.loads(out)) == "New maps for Fake Game: 1\nNew items for Fake Game: 3"


@pytest.mark.parametrize("why", ["running", "updating"])
def test_check_new_skips_a_busy_game(tmp_path, capsys, monkeypatch, quiet, why):
    game = make_game(tmp_path)
    spec = content_spec(game)
    if why == "running":
        monkeypatch.setattr(app_guard, "game_running", lambda install, exes=None: True)
    else:
        monkeypatch.setattr(app_guard, "game_updating", lambda install, now=None: True)
    code, out = run(spec, "check-new", "--json", "--auto-extract", capsys=capsys)
    g = json.loads(out)["games"][0]
    assert code == 0 and g["skipped"] == why and g["auto_extracted"] == [] and g["new_maps"] == []
    assert not (tmp_path / "levels" / "fake" / "alpha").exists()
    assert app_tray.new_content_text(json.loads(out)) == ""
    # the tool's own `running` hook decides when it has one
    monkeypatch.setattr(app_guard, "game_updating", lambda install, now=None: False)
    spec.games[0].running = lambda install: False
    _, out = run(spec, "check-new", "--json", capsys=capsys)
    assert json.loads(out)["games"][0]["skipped"] is None


def test_guard_running_and_updating(tmp_path):
    G = app_guard
    game = tmp_path / "lib" / "steamapps" / "common" / "Some Game"
    (game / "bin").mkdir(parents=True)
    assert G.game_running(game, exes=[str(game / "bin" / "game.exe")])
    assert not G.game_running(game, exes=[str(tmp_path / "lib" / "other.exe"), str(game) + "2/x.exe"])
    acf = tmp_path / "lib" / "steamapps" / "appmanifest_4242.acf"
    acf.write_text('"AppState"\n{\n "appid" "4242"\n "installdir" "Some Game"\n "StateFlags" "4"\n}\n')
    assert not G.game_updating(game) and not G.game_updating(game / "bin")
    acf.write_text(acf.read_text().replace('"StateFlags" "4"', '"StateFlags" "1026"'))
    assert G.game_updating(game / "bin")
    acf.write_text(acf.read_text().replace('"StateFlags" "1026"', '"StateFlags" "4"'))
    (tmp_path / "lib" / "steamapps" / "downloading" / "4242").mkdir(parents=True)
    assert G.game_updating(game)
    # other stores: a file in the top two levels written in the last 10 minutes
    other = tmp_path / "Games" / "Other"
    (other / "data" / "deep").mkdir(parents=True)
    (other / "data" / "deep" / "pak.bin").write_bytes(b"x")
    old = time.time() - 3600
    for p in (other / "data" / "deep" / "pak.bin", other / "data" / "deep", other / "data"):
        os.utime(p, (old, old))
    assert not G.game_updating(other)  # a fresh file three levels down is not looked at
    (other / "data" / "new.pak").write_bytes(b"x")
    assert G.game_updating(other) and not G.game_updating(other, now=time.time() + 3600)
    # the real process list: readable, and nothing runs from a folder made just now
    if os.name == "nt" or os.path.isdir("/proc"):
        assert G.process_exes()
    assert not G.game_running(other)


def test_tray_tells_new_content_once(tmp_path):
    f = tmp_path / "s.json"
    w = app_tray.StatusWatch(f)
    assert w.poll() is None
    doc = {"games": [{"game": "fake", "label": "Fake Game", "skipped": None, "new_maps": ["a", "b"],
                      "auto_extracted": [], "items": {"new_count": 0}}]}
    f.write_text(json.dumps(doc))
    assert w.poll() == "New maps for Fake Game: 2"
    t = time.time() + 5
    os.utime(f, (t, t))
    assert w.poll() is None  # the same finding is told once


def test_plugin_manifest_names_this_tool():
    """`plugin.json` (3DHeat's docs/plugins.md): this tool as its main program, every capability a program of it.
    The archive carries it beside the program (tools/build_standalone.py)."""
    manifest = ROOT / "plugin.json"
    if not manifest.is_file():
        pytest.skip("no plugin.json in this repository")
    import importlib.util

    spec_mod = importlib.util.spec_from_file_location("build_standalone", ROOT / "tools" / "build_standalone.py")
    build = importlib.util.module_from_spec(spec_mod)
    spec_mod.loader.exec_module(build)
    real = importlib.import_module(CFG["spec"]).SPEC
    m = json.loads(manifest.read_text(encoding="utf-8"))
    build.check_plugin(m, real)
    if real.replays is not None:
        caps = m["capabilities"]
        assert "replays" in caps, "a tool that converts replays says so in plugin.json"
        exts = {e.lstrip(".") for e in real.replays.extensions}
        pats = {p.split("*.")[-1] for r in m.get("replays", []) for p in r["patterns"]}
        assert exts <= pats, f"plugin.json lists the replay files {sorted(pats)}, the tool reads {sorted(exts)}"
