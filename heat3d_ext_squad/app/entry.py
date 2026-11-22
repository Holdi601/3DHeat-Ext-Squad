"""
The standalone executable's command line (the same in every 3DHeat extractor).

    <id>                      the window (gui.py)
    <id> --version | --help
    <id> --check --json       what is found and what is missing, as JSON
    <id> status [--json]      maps new / changed / outdated / current per game
    <id> extract [--new] [--changed] [--outdated] [--all] [<map>...] [--game G] [--progress-json]
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
import importlib
import json
import os
import sys
from pathlib import Path

from . import paths, update
from .manifest import Manifest, game_status
from .spec import Spec, game_folders, standard_checks

APP_FLAGS = ("--version", "-V", "--help", "-h", "--check", "--gui-selftest", "--update")
APP_VERBS = ("status", "extract", "convert", "info")


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
        games.append(s)
    return {"id": spec.id, "version": spec.version, "levels": str(levels), "games": games}


def extract(spec: Spec, *, game_key: str | None, ids: list[str], states: set[str], progress_json: bool,
            log=None) -> int:
    """Extract the chosen maps one at a time; the manifest is written after each."""
    levels = paths.levels_dir()
    found = game_folders(spec)
    emit = (lambda d: print(json.dumps(d), flush=True)) if progress_json else (lambda d: None)
    say = log or ((lambda s: print(s, file=sys.stderr, flush=True)) if progress_json else (lambda s: print(s, flush=True)))
    jobs = []
    for g in spec.games:
        if (game_key and g.key != game_key) or g.maps is None or g.extract is None:
            continue
        game = found.get(g.key)
        if game is None:
            if game_key or ids:
                say(f"{g.label} not found")
            continue
        st = game_status(g, game, levels, spec.id)
        for m in st["_states"]:
            if m.source is None:
                continue
            if m.id in ids or m.state in states:
                jobs.append((g, game, m, st["build"]))
    if not jobs:
        say("nothing to extract" if spec.has_maps() else f"{spec.name} reads no maps; nothing to extract")
        emit({"event": "start", "total": 0})
        emit({"event": "done", "ok": 0, "failed": 0})
        return 0
    emit({"event": "start", "total": len(jobs)})
    ok = failed = 0
    for i, (g, game, m, build) in enumerate(jobs, 1):
        out = levels / g.subdir if g.subdir else levels
        say(f"[{i}/{len(jobs)}] {g.label}: {m.title} ({m.state})")
        try:
            outputs = g.extract(game, m.source, out, say)
            man = Manifest(out, spec.id)
            man.record(game, m.source, outputs, spec.version, build, levels)
            man.save()
            ok += 1
            emit({"event": "map", "index": i, "id": m.id, "state": "ok", "detail": f"{len(outputs)} files"})
        except Exception as e:
            failed += 1
            say(f"failed {m.id}: {type(e).__name__}: {e}")
            emit({"event": "map", "index": i, "id": m.id, "state": "failed", "detail": f"{type(e).__name__}: {e}"})
    emit({"event": "done", "ok": ok, "failed": failed})
    say(f"{ok} extracted, {failed} failed")
    return 1 if failed else 0


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
                      + (f" - {c['new']} new, {c['changed']} changed, {c['outdated']} outdated, {c['current']} current"
                         + (f", {c['missing']} gone from the install" if c["missing"] else "") if g["maps"] else ""))
                for m in g["maps"]:
                    if m["state"] != "current":
                        print(f"  {m['state']:<9} {m['id']}")
        return 0
    if head == "extract":
        ap = argparse.ArgumentParser(prog=f"{spec.id} extract")
        ap.add_argument("maps", nargs="*")
        ap.add_argument("--game")
        for s in ("new", "changed", "outdated"):
            ap.add_argument(f"--{s}", action="store_true")
        ap.add_argument("--all", action="store_true", help="every map, also the current ones")
        ap.add_argument("--progress-json", action="store_true")
        a = ap.parse_args(argv[1:])
        states = {s for s in ("new", "changed", "outdated") if getattr(a, s)}
        if a.all:
            states = {"new", "changed", "outdated", "current"}
        if not states and not a.maps:
            states = {"new"}
        return extract(spec, game_key=a.game, ids=a.maps, states=states, progress_json=a.progress_json)
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
