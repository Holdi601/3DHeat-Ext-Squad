"""
The standalone app's description of this tool (app/spec.py): Squad demos are
recorded on a server, so there are no maps to extract; the window finds a
Squad server (or game) install on this machine for its demo folder and runs
the demo conversion as a task. `python -m heat3d_ext_squad.standalone_spec`
runs the app from a checkout; the release executables run the same.
"""

from __future__ import annotations

from pathlib import Path

from . import __version__
from .app import paths
from .app.spec import GameSpec, Input, Replays, Spec, Task, game_folders

TOOL = "heat3d-squad-demo"
#: The Steam folders a Squad server or the game itself installs into.
STEAM_FOLDERS = ("Squad Dedicated Server", "Squad")


def demo_folder(install: Path) -> Path:
    """Where a Squad server writes its demos."""
    return install / "SquadGame" / "Saved" / "Demos"


def _is_install(p: Path) -> bool:
    return (p / "SquadGame").is_dir()


def _find(given: str | None) -> Path | None:
    if given:
        p = Path(given).expanduser()
        # The install, or its demo folder itself.
        for candidate in (p, *p.parents[:3]):
            if _is_install(candidate):
                return candidate
        return None
    return paths.first([d for name in STEAM_FOLDERS for d in paths.steam_game_dirs(name)], _is_install)


def _default_demos(levels: Path) -> str:
    install = game_folders(SPEC).get("squad")
    if install is not None and demo_folder(install).is_dir():
        return str(demo_folder(install))
    return ""

def _replay_info(path: Path) -> dict:
    """`info <replay> --json`: the header only (replay_info.py)."""
    from .replay_info import info

    return info(path)


SPEC = Spec(
    id="heat3d-squad",
    name="3DHeat Squad",
    repo="Holdi601/3DHeat-Ext-Squad",
    version=__version__,
    tools={TOOL: "heat3d_ext_squad.cli:main"},
    default_tool=TOOL,
    description="Squad server demos into 3DHeat heatmap tables",
    module="heat3d_ext_squad.standalone_spec",
    games=[GameSpec(key="squad", label="Squad server", find=_find, subdir="squad",
                    platforms=("windows-x64", "linux-x64"))],
    tasks=[Task(
        "demos", "Convert demos",
        [Input("src", "Folder with .replay demos", "folder", default=_default_demos),
         Input("out", "Where the matches go", "folder",
               default=lambda levels: str(paths.data_dir() / "matches" / "squad"))],
        lambda v, levels: [TOOL, v["src"], "-o", v["out"]],
        help="each demo becomes a heatmap table and a match document the viewer opens",
    )],
    min_free_gb=1.0,
    replays=Replays("squad", (".replay",), lambda r, out: [TOOL, str(r), "-o", str(out)], info=_replay_info),
    notice="Not affiliated with or endorsed by Offworld Industries.",
)

if __name__ == "__main__":
    from .app.entry import main
    from .update import apply

    raise SystemExit(main(SPEC, apply_source=apply))
