"""
`heat3d-squad-demo <demos> -o <outdir>`: Squad server demos into heatmap tables.

Each `.replay` (or every `.replay` in a folder given) becomes
`<outdir>/<map>/<name>.parquet` and `<outdir>/<map>/<name>.match.json`, as the
CS2 tool writes them (`--flat` leaves out the map folder), with the sidecars
`<name>.entities.parquet` and `<name>.packets.parquet` beside them. A demo that cannot
be read is reported and skipped; the exit code is 1 if any was, 0 otherwise.
`--json` prints one line of JSON per demo instead of text, for callers such as
the 3DHeat Watcher.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .bits import ReadError
from .output import write
from .squad import load


def demos(paths: list[str]) -> list[Path]:
    out: list[Path] = []
    for p in map(Path, paths):
        if p.is_dir():
            out.extend(sorted(p.glob("*.replay")))
        else:
            out.append(p)
    return out


def map_folder(level: str) -> str:
    """`/Game/Maps/<Map>/Gameplay_Layers/<Layer>` -> `<Map>`; the level's last part otherwise."""
    parts = [p for p in level.split("/") if p]
    if len(parts) >= 3 and parts[:2] == ["Game", "Maps"]:
        return parts[2]
    return parts[-1] if parts else "unknown"


def main(argv: list[str] | None = None) -> int:
    # A newer release is offered, and installed only if the user says yes (notified only when nobody can be asked).
    try:
        import heat3d_update

        heat3d_update.startup("heat3d_ext_squad")
    except Exception:  # an update check never stops a conversion
        pass
    ap = argparse.ArgumentParser(prog="heat3d-squad-demo", description="Squad server demos (.replay) into "
                                 "3DHeat heatmap tables: every player's position, team and squad.")
    ap.add_argument("demos", nargs="+", help=".replay files, or folders holding them")
    ap.add_argument("-o", "--out", required=True, help="folder for <map>/<name>.parquet and .match.json")
    ap.add_argument("--flat", action="store_true", help="write straight into the folder, without <map>/")
    ap.add_argument("--json", action="store_true", help="one line of JSON per demo on stdout")
    ap.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = ap.parse_args(argv)
    failed = 0
    files = demos(args.demos)
    if not files:
        print("no .replay files found", file=sys.stderr)
        return 1
    for f in files:
        try:
            m = load(f)
            folder = Path(args.out) if args.flat else Path(args.out) / map_folder(m.level)
            data, doc = write(m, folder)
        except (OSError, ReadError) as e:
            failed += 1
            if args.json:
                print(json.dumps({"demo": str(f), "ok": False, "error": str(e)}), flush=True)
            else:
                print(f"{f.name}: not read - {e}", file=sys.stderr)
            continue
        summary = json.loads(doc.read_text(encoding="utf-8"))
        if args.json:
            print(json.dumps({"demo": str(f), "ok": True, "parquet": str(data), "match": str(doc),
                              "sidecars": [str(data.parent / x) for x in m.sidecars],
                              "lost": summary["selfCheck"]["completeness"].get("lost"),
                              "rows": summary["rows"], "players": len(summary["players"]),
                              "layer": summary["layer"], "recorded_unix": summary["recorded_unix"]}), flush=True)
        else:
            print(f"{f.name}: {summary['layer']}, {len(summary['players'])} players, {summary['rows']} rows -> {data}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
