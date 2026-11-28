"""
The standalone executable's command line (the same in every 3DHeat extractor).

    <id>                      the window (gui.py)
    <id> --version | --help
    <id> --check --json       what is found and what is missing, as JSON
    <id> status [--json]      maps (and other content) new / changed / outdated / current per game
    <id> extract [--new] [--changed] [--outdated] [--all] [--content] [<map>|content:<id>...] [--game G]
                 [--progress-json]
    <id> check-new [--json] [--auto-extract] [--game G]   the unattended check: low priority, no window,
                              skips a game that runs or updates, writes <levels>/.heat3d-status/<id>.json
    <id> convert <replay>... -o <out> [--progress-json]   replay readers: replays into matches
    <id> info <replay> --json  replay readers: what a replay holds, without converting it
    <id> --update             look for a newer release and apply it (asks first)
    <id> --gui-selftest       build the window's model without showing it (CI)
    <id> <tool> [args...]     one of the tool's own commands, unchanged
    <id> [args...]            the main command, unchanged

`--auto-update` before any of these applies a newer release without asking (this run).
"""

from __future__ import annotations

import argparse
import datetime as _dt
import importlib
import json
import os
import sys
from pathlib import Path

from . import guard, paths, update
from .manifest import CONTENT, STATES, Manifest, game_status, item_diff
from .spec import Spec, game_folders, standard_checks

APP_FLAGS = ("--version", "-V", "--help", "-h", "--check", "--gui-selftest", "--update")
APP_VERBS = ("status", "extract", "convert", "info", "check-new")
STATUS_DIR = ".heat3d-status"
STATUS_FORMAT = "3dheat-content-status"


def target(spec: Spec, apply_source=None) -> update.Target:
    return update.Target(spec.repo, spec.id, spec.name, spec.version, apply_source)


def run_tool(spec: Spec, tool: str, argv: list[str]) -> int:
    mod, _, fn = spec.tools[tool].partition(":")
    func = getattr(importlib.import_module(mod), fn or "main")
    old = sys.argv
    sys.argv = [tool, *argv]
    try:
        code = func(argv)
    except SystemExit as e:
        code = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
    finally:
        sys.argv = old
    return int(code or 0)


def _usage(spec: Spec) -> str:
    tools = "\n".join(f"  {spec.id} {t} [args...]" for t in spec.tools)
    if spec.replays is not None:
        tools = (f"  {spec.id} convert REPLAY... -o OUT [--progress-json]   replays into 3DHeat matches\n"
                 f"  {spec.id} info REPLAY --json   what a replay holds, without converting it\n") + tools
    return f"""{spec.name} {spec.version}{(' - ' + spec.description) if spec.description else ''}

  {spec.id}                    open the window
  {spec.id} --version
  {spec.id} --check --json     what is found and what is missing
  {spec.id} status [--json]    maps that are new, changed or extracted by an older version
  {spec.id} extract [--new] [--changed] [--outdated] [--all] [MAP...] [--game KEY] [--progress-json]
  {spec.id} extract --content ...    the same for other content (catalogue, models); content:ID for one
  {spec.id} check-new [--json] [--auto-extract] [--game KEY]   look for new content, unattended
  {spec.id} --update           look for a newer release and apply it
  {spec.id} --auto-update ...  apply a newer release without asking (this run)
{tools}
  {spec.id} [args...]          same as `{spec.id} {spec.default_tool} [args...]`

Writes into the levels folder: {paths.levels_dir()} (HEAT3D_LEVELS changes it).
"""


def check_doc(spec: Spec) -> dict:
    levels = paths.levels_dir()
    found = game_folders(spec)
    return {"id": spec.id, "version": spec.version, "levels": str(levels),
            "checks": [c.__dict__ for c in standard_checks(spec, found, levels)]}


def status_doc(spec: Spec, game_key: str | None = None) -> dict:
    levels = paths.levels_dir()
    found = game_folders(spec)
    games = []
    for g in spec.games:
        if game_key and g.key != game_key:
            continue
        s = game_status(g, found.get(g.key), levels, spec.id)
        s.pop("_states", None)
        s.pop("_content_states", None)
        games.append(s)
    return {"id": spec.id, "version": spec.version, "levels": str(levels), "games": games}


def _jobs(spec: Spec, levels: Path, found: dict, *, game_key: str | None, ids: list[str], states: set[str],
          content: bool, say) -> list[tuple]:
    """(game spec, install, state, build, is content) for every map and content entry chosen."""
    jobs = []
    for g in spec.games:
        has_maps = g.maps is not None and g.extract is not None
        has_content = g.contents is not None and g.extract_content is not None
        if (game_key and g.key != game_key) or not (has_maps or has_content):
            continue
        game = found.get(g.key)
        if game is None:
            if game_key or ids:
                say(f"{g.label} not found")
            continue
        st = game_status(g, game, levels, spec.id)
        if has_maps:
            for m in st["_states"]:
                if m.source is not None and (m.id in ids or m.state in states):
                    jobs.append((g, game, m, st["build"], False))
        if has_content:
            for c in st["_content_states"]:
                if c.source is not None and (CONTENT + c.id in ids or (content and c.state in states)):
                    jobs.append((g, game, c, st["build"], True))
    return jobs


def run_jobs(spec: Spec, levels: Path, jobs: list[tuple], emit, say) -> tuple[list[str], list[dict]]:
    """Extract each job, the manifest written after each: (ids done, [{"id", "detail"} failed])."""
    done: list[str] = []
    failed: list[dict] = []
    for i, (g, game, m, build, is_content) in enumerate(jobs, 1):
        out = levels / g.subdir if g.subdir else levels
        jid = CONTENT + m.id if is_content else m.id
        say(f"[{i}/{len(jobs)}] {g.label}: {m.title} ({m.state})")
        try:
            outputs = (g.extract_content if is_content else g.extract)(game, m.source, out, say)
            man = Manifest(out, spec.id)
            man.record(game, m.source, outputs, spec.version, build, levels)
            man.save()
            done.append(jid)
            emit({"event": "map", "index": i, "id": jid, "state": "ok", "detail": f"{len(outputs)} files"})
        except Exception as e:
            failed.append({"id": jid, "detail": f"{type(e).__name__}: {e}"})
            say(f"failed {jid}: {type(e).__name__}: {e}")
            emit({"event": "map", "index": i, "id": jid, "state": "failed", "detail": f"{type(e).__name__}: {e}"})
    return done, failed


def extract(spec: Spec, *, game_key: str | None, ids: list[str], states: set[str], progress_json: bool,
            log=None, content: bool = False) -> int:
    """Extract the chosen maps (and, with `content`, content entries) one at a time."""
    levels = paths.levels_dir()
    found = game_folders(spec)
    emit = (lambda d: print(json.dumps(d), flush=True)) if progress_json else (lambda d: None)
    say = log or ((lambda s: print(s, file=sys.stderr, flush=True)) if progress_json else (lambda s: print(s, flush=True)))
    jobs = _jobs(spec, levels, found, game_key=game_key, ids=ids, states=states, content=content, say=say)
    if not jobs:
        say("nothing to extract" if spec.has_maps() or spec.has_content() else f"{spec.name} reads no maps; nothing to extract")
        emit({"event": "start", "total": 0})
        emit({"event": "done", "ok": 0, "failed": 0})
        return 0
    emit({"event": "start", "total": len(jobs)})
    done, failed = run_jobs(spec, levels, jobs, emit, say)
    emit({"event": "done", "ok": len(done), "failed": len(failed)})
    say(f"{len(done)} extracted, {len(failed)} failed")
    return 1 if failed else 0


# ------------------------------------------------------------------ check-new


def status_file(spec: Spec, levels: Path | None = None) -> Path:
    return Path(levels or paths.levels_dir()) / STATUS_DIR / f"{spec.id}.json"


def _now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _check_game(spec: Spec, g, game: Path | None, levels: Path, auto_extract: bool, say) -> dict:
    zero = {s: 0 for s in STATES}
    e: dict = {"game": g.key, "label": g.label, "found": game is not None, "build": None, "build_changed": False,
               "skipped": None, "counts": dict(zero), "content_counts": dict(zero), "items": item_diff({}, {}),
               "new_maps": [], "replace_maps": [], "new_content": [], "replace_content": [],
               "auto_extracted": [], "failed": []}
    if game is None:
        return e
    why = guard.skip_reason(g, game)
    if why:
        e["skipped"] = why
        if g.build is not None:
            try:
                e["build"] = g.build(game)
            except Exception:
                pass
        return e

    def fill(st: dict) -> None:
        for k in ("build", "build_changed", "counts", "content_counts", "items"):
            e[k] = st[k]
        e["new_maps"] = [m.id for m in st["_states"] if m.state == "new"]
        e["replace_maps"] = [m.id for m in st["_states"] if m.state in ("changed", "outdated")]
        e["new_content"] = [CONTENT + c.id for c in st["_content_states"] if c.state == "new"]
        e["replace_content"] = [CONTENT + c.id for c in st["_content_states"] if c.state in ("changed", "outdated")]

    try:
        st = game_status(g, game, levels, spec.id)
    except Exception as x:
        e["failed"].append({"id": "status", "detail": f"{type(x).__name__}: {x}"})
        return e
    fill(st)
    if not auto_extract:
        return e
    # Purely additive: never-extracted maps and content whose outputs do not exist yet. Anything that would
    # replace files (changed, outdated) stays listed for the user to confirm.
    jobs = []
    if g.maps is not None and g.extract is not None:
        jobs += [(g, game, m, st["build"], False) for m in st["_states"] if m.state == "new" and m.source is not None]
    if g.contents is not None and g.extract_content is not None:
        jobs += [(g, game, c, st["build"], True) for c in st["_content_states"]
                 if c.state == "new" and c.source is not None]
    if not jobs:
        return e
    before = e["items"]
    done, failed = run_jobs(spec, levels, jobs, lambda d: None, say)
    e["failed"] += failed
    try:
        fill(game_status(g, game, levels, spec.id))
    except Exception as x:
        e["failed"].append({"id": "status", "detail": f"{type(x).__name__}: {x}"})
    e["auto_extracted"] = done
    if any(j.startswith(CONTENT) for j in done) and before.get("new_count"):
        e["auto_extracted_items"] = {"new": before["new"], "new_count": before["new_count"]}
    return e


def write_status(spec: Spec, levels: Path, games: list[dict]) -> dict:
    """`<levels>/.heat3d-status/<id>.json`, written atomically; games not checked this time are kept."""
    f = status_file(spec, levels)
    kept: dict[str, dict] = {}
    try:
        old = json.loads(f.read_text(encoding="utf-8"))
        if isinstance(old, dict) and old.get("format") == STATUS_FORMAT:
            kept = {x["game"]: x for x in old.get("games", []) if isinstance(x, dict) and "game" in x}
    except (OSError, ValueError):
        pass
    kept.update({x["game"]: x for x in games})
    order = [g.key for g in spec.games]
    doc = {"format": STATUS_FORMAT, "version": 1, "tool": spec.id, "toolVersion": spec.version, "at": _now_iso(),
           "games": sorted(kept.values(), key=lambda x: order.index(x["game"]) if x["game"] in order else len(order))}
    f.parent.mkdir(parents=True, exist_ok=True)
    tmp = f.with_name(f"{f.name}.{os.getpid()}.tmp")
    tmp.write_text(json.dumps(doc, indent=1), encoding="utf-8")
    os.replace(tmp, f)
    return doc


def check_new(spec: Spec, *, game_key: str | None = None, auto_extract: bool = False, say=None) -> dict:
    """The unattended check: at low priority, each game skipped while it runs or updates, the status file written."""
    say = say or (lambda s: print(s, file=sys.stderr, flush=True))
    guard.lower_priority()
    levels = paths.levels_dir()
    found = game_folders(spec)
    games = [_check_game(spec, g, found.get(g.key), levels, auto_extract, say)
             for g in spec.games if not game_key or g.key == game_key]
    return write_status(spec, levels, games)


def _check_line(e: dict) -> str:
    if not e["found"]:
        return f"{e['label']}: not found"
    if e["skipped"]:
        return f"{e['label']}: not checked now, the game is {e['skipped']}"
    bits = [f"{len(e['new_maps'])} new maps"]
    if e["replace_maps"]:
        bits.append(f"{len(e['replace_maps'])} to extract again (asks first)")
    if e["new_content"] or e["replace_content"]:
        bits.append(f"{len(e['new_content'])} new and {len(e['replace_content'])} changed content")
    if e["items"].get("new_count"):
        bits.append(f"{e['items']['new_count']} new items")
    if e["auto_extracted"]:
        bits.append(f"{len(e['auto_extracted'])} extracted now")
    if e["failed"]:
        bits.append(f"{len(e['failed'])} failed")
    return f"{e['label']}: " + ", ".join(bits) + (" (new game build)" if e["build_changed"] else "")


INFO_KEYS = ("game", "map", "mode", "date", "duration_s", "players", "teams", "outcome", "game_version")


def convert(spec: Spec, inputs: list[str], out: str, progress_json: bool) -> int:
    """`convert <replay>... -o <out>`: each replay through the tool's own converter, one at a time."""
    import contextlib

    r = spec.replays
    emit = (lambda d: print(json.dumps(d), flush=True)) if progress_json else (lambda d: None)
    emit({"event": "start", "total": len(inputs)})
    ok = failed = 0
    Path(out).mkdir(parents=True, exist_ok=True)
    for i, inp in enumerate(inputs, 1):
        argv = r.convert(Path(inp), Path(out))
        # with --progress-json, stdout carries only the JSON lines; the tool's own words go to stderr
        with contextlib.redirect_stdout(sys.stderr) if progress_json else contextlib.nullcontext():
            try:
                code = run_tool(spec, argv[0], [str(a) for a in argv[1:]])
                detail = "" if code == 0 else f"exit {code}"
            except Exception as e:  # a replay that breaks the reader fails alone
                code, detail = 1, f"{type(e).__name__}: {e}"
        ok, failed = ok + (code == 0), failed + (code != 0)
        emit({"event": "file", "index": i, "input": inp, "state": "ok" if code == 0 else "failed", "detail": detail})
        emit({"progress": round(i / len(inputs), 4)})
    emit({"event": "done", "ok": ok, "failed": failed})
    return 0 if failed == 0 else 1


def info_doc(spec: Spec, replay: str) -> dict:
    """`info <replay> --json`: the match a replay holds, as far as it can be read without converting it."""
    r = spec.replays
    p = Path(replay)
    doc: dict = {k: None for k in INFO_KEYS}
    doc.update(players=[], teams=[], game=r.game)
    complete = False
    if r.info is not None:
        got = r.info(p) or {}
        doc.update({k: v for k, v in got.items() if v is not None})
        complete = True
    if doc["date"] is None:
        try:
            from datetime import datetime, timezone

            doc["date"] = datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).isoformat(timespec="seconds")
            doc["date_from"] = "file"
        except OSError:
            pass
    doc.update(file=p.name, size=p.stat().st_size if p.exists() else None,
               converter={"id": spec.id, "version": spec.version}, complete=complete)
    return doc


def _console_streams(cli: bool) -> None:
    """The Windows build is a window program (no console window on a double-click). On the command line it
    writes into the console it was started from; into pipes when a program runs it; nowhere when neither."""
    if os.name != "nt":
        return
    try:
        import ctypes

        k = ctypes.windll.kernel32
        attached = False
        if cli and (sys.stdout is None or sys.stderr is None) and k.AttachConsole(-1):  # ATTACH_PARENT_PROCESS
            attached = True

        def stream(name: str, mode: str):
            try:
                return open(name if attached else os.devnull, mode, encoding="utf-8", errors="replace",
                            buffering=1 if "w" in mode else -1)
            except OSError:
                return open(os.devnull, mode)

        if sys.stdout is None:
            sys.stdout = stream("CONOUT$", "w")
        if sys.stderr is None:
            sys.stderr = stream("CONOUT$", "w")
        if sys.stdin is None:
            sys.stdin = stream("CONIN$", "r")
        if not k.GetConsoleWindow():
            # No console: console programs this one starts (a tool's helpers) would each open a window.
            import subprocess

            if not getattr(subprocess.Popen, "_heat3d_no_window", False):
                orig = subprocess.Popen.__init__

                def init(self, *a, **kw):
                    if not kw.get("creationflags"):
                        kw["creationflags"] = subprocess.CREATE_NO_WINDOW
                    orig(self, *a, **kw)

                subprocess.Popen.__init__ = init
                subprocess.Popen._heat3d_no_window = True
    except Exception:
        pass


def main(spec: Spec, argv: list[str] | None = None, apply_source=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    _console_streams(cli=bool(argv))
    if "--auto-update" in argv:
        argv.remove("--auto-update")
        update.AUTO_THIS_RUN = True
    t = target(spec, apply_source)
    if not argv:
        from . import gui

        return gui.run(spec, t)
    head = argv[0]
    if head in ("--version", "-V"):
        print(f"{spec.id} {spec.version}")
        return 0
    if head in ("--help", "-h"):
        print(_usage(spec))
        return 0
    if head == "--gui-selftest":
        from . import gui

        return gui.selftest(spec, t)
    if head == "--check":
        doc = check_doc(spec)
        if "--json" in argv:
            print(json.dumps(doc))
        else:
            for c in doc["checks"]:
                print(f"{'ok ' if c['ok'] else 'MISSING'}  {c['label']}: {c['detail']}")
        return 0
    if head == "--update":
        r = update.available(t, use_cache=False, include_skipped=True)
        if r is None:
            print(f"{spec.name} {spec.version} is the newest published version.")
            return 0
        print(update.notice(t, r))
        if not update.auto_enabled(spec.id):
            try:
                if input("Update now? [y/N] ").strip().lower() not in ("y", "yes", "j", "ja"):
                    return 0
            except EOFError:
                return 0
        try:
            print(update.apply(t, r))
        except RuntimeError as e:
            print(f"update not applied: {e}", file=sys.stderr)
            return 1
        return 0
    if head == "status":
        ap = argparse.ArgumentParser(prog=f"{spec.id} status")
        ap.add_argument("--json", action="store_true")
        ap.add_argument("--game")
        a = ap.parse_args(argv[1:])
        doc = status_doc(spec, a.game)
        if a.json:
            print(json.dumps(doc))
        else:
            for g in doc["games"]:
                c = g["counts"]
                print(f"{g['label']}: {'found' if g['found'] else 'not found'}"
                      + (f", build {g['build']}" if g.get("build") else "")
                      + (" (new since the last extract)" if g.get("build_changed") else "")
                      + (f" - {c['new']} new, {c['changed']} changed, {c['outdated']} outdated, {c['current']} current"
                         + (f", {c['missing']} gone from the install" if c["missing"] else "") if g["maps"] else ""))
                for m in g["maps"]:
                    if m["state"] != "current":
                        print(f"  {m['state']:<9} {m['id']}")
                for m in g.get("content", []):
                    print(f"  {m['state']:<9} {CONTENT}{m['id']} ({m['kind']})")
                it = g.get("items") or {}
                if it.get("new_count") or it.get("gone_count"):
                    print(f"  items: {it['new_count']} new in the install"
                          + (f", {it['gone_count']} gone" if it["gone_count"] else "")
                          + "".join(f"; {k}: {', '.join(v[:5])}{' ...' if len(v) > 5 else ''}" for k, v in it["new"].items()))
        return 0
    if head == "check-new":
        ap = argparse.ArgumentParser(prog=f"{spec.id} check-new",
                                     description="Look for new maps and content, unattended (low priority, no window).")
        ap.add_argument("--json", action="store_true")
        ap.add_argument("--auto-extract", action="store_true",
                        help="extract what is new and not extracted yet (never replaces files)")
        ap.add_argument("--game")
        a = ap.parse_args(argv[1:])
        import contextlib

        try:  # a tool's extract that prints goes to stderr: stdout carries only the answer
            with contextlib.redirect_stdout(sys.stderr):
                doc = check_new(spec, game_key=a.game, auto_extract=a.auto_extract)
        except OSError as e:  # the status file could not be written
            print(f"check-new: {type(e).__name__}: {e}", file=sys.stderr)
            return 1
        if a.json:
            print(json.dumps(doc))
        else:
            for e in doc["games"]:
                print(_check_line(e))
        return 0
    if head == "extract":
        ap = argparse.ArgumentParser(prog=f"{spec.id} extract")
        ap.add_argument("maps", nargs="*")
        ap.add_argument("--game")
        for s in ("new", "changed", "outdated"):
            ap.add_argument(f"--{s}", action="store_true")
        ap.add_argument("--all", action="store_true", help="every map, also the current ones")
        ap.add_argument("--content", action="store_true",
                        help="content (catalogue, models) too, by the same states; content:ID picks one")
        ap.add_argument("--progress-json", action="store_true")
        a = ap.parse_args(argv[1:])
        states = {s for s in ("new", "changed", "outdated") if getattr(a, s)}
        if a.all:
            states = {"new", "changed", "outdated", "current"}
        if not states and not a.maps:
            states = {"new"}
        return extract(spec, game_key=a.game, ids=a.maps, states=states, progress_json=a.progress_json,
                       content=a.content)
    if head == "convert" and spec.replays is not None:
        ap = argparse.ArgumentParser(prog=f"{spec.id} convert", description="Convert replays into 3DHeat matches.")
        ap.add_argument("inputs", nargs="+", help="replay files")
        ap.add_argument("-o", "--out", required=True, help="folder for the converted matches")
        ap.add_argument("--progress-json", action="store_true")
        a = ap.parse_args(argv[1:])
        return convert(spec, a.inputs, a.out, a.progress_json)
    if head == "info" and spec.replays is not None:
        ap = argparse.ArgumentParser(prog=f"{spec.id} info", description="What a replay holds, without converting it.")
        ap.add_argument("replay")
        ap.add_argument("--json", action="store_true")
        a = ap.parse_args(argv[1:])
        try:
            doc = info_doc(spec, a.replay)
        except Exception as e:  # unreadable: say so, as JSON when asked
            doc = {"error": f"{type(e).__name__}: {e}", "file": Path(a.replay).name}
            print(json.dumps(doc) if a.json else doc["error"])
            return 1
        if a.json:
            print(json.dumps(doc, default=str))
        else:
            for k, v in doc.items():
                if v not in (None, [], {}):
                    print(f"{k}: {v}")
        return 0
    # The tools announce updates themselves (their own startup check, the same policy).
    if head in spec.tools:
        return run_tool(spec, head, argv[1:])
    return run_tool(spec, spec.default_tool, argv)
