"""The standalone app's own parts, on a synthetic game install (no game files)."""

from __future__ import annotations

import hashlib
import importlib
import io
import json
import os
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
    _, text = run(fake_spec(game), "status", "--json", capsys=capsys)
    assert json.loads(text)["games"][0]["maps"][0]["state"] == "outdated"


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
