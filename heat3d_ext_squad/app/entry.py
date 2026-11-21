"""
The standalone executable's command line (the same in every 3DHeat extractor).

    <id>                      the window (gui.py)
    <id> --version | --help
    <id> --check --json       what is found and what is missing, as JSON
    <id> status [--json]      maps new / changed / outdated / current per game
    <id> extract [--new] [--changed] [--outdated] [--all] [<map>...] [--game G] [--progress-json]
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
APP_VERBS = ("status", "extract")


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


def _hide_own_console() -> None:
    """Started by a double-click, a console program brings a console window; the window app hides it."""
    if os.name != "nt" or not update.frozen():
        return
    try:
        import ctypes

        k = ctypes.windll.kernel32
        buf = (ctypes.c_uint * 4)()
        if k.GetConsoleProcessList(buf, 4) <= 1:  # nobody else shares it: it is ours alone
            hwnd = k.GetConsoleWindow()
            if hwnd:
                ctypes.windll.user32.ShowWindow(hwnd, 0)
    except Exception:
        pass


def main(spec: Spec, argv: list[str] | None = None, apply_source=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--auto-update" in argv:
        argv.remove("--auto-update")
        update.AUTO_THIS_RUN = True
    t = target(spec, apply_source)
    if not argv:
        _hide_own_console()
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
    # The tools announce updates themselves (their own startup check, the same policy).
    if head in spec.tools:
        return run_tool(spec, head, argv[1:])
    return run_tool(spec, spec.default_tool, argv)
