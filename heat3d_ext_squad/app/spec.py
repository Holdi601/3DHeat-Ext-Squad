"""
What a tool tells the standalone app about itself (its `standalone_spec.py`).

The app (entry.py, gui.py) is the same in every 3DHeat extractor; a spec is
the only part each one writes: its name and repository, its command-line tools,
the games it reads and how to find them, the checks before it can run, and, for
map extractors, the maps an install holds and how one is extracted; for
catalogue and model extractors, the other content an install holds (a
catalogue, a model pack, a gadget list: `GameSpec.contents`).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from . import paths


@dataclass
class Check:
    id: str
    label: str
    ok: bool
    detail: str = ""


@dataclass
class MapSource:
    """One map (or other content) in an install: its id (the output's name), a title, and the game files it is made from."""

    id: str
    title: str
    sources: list[Path]
    #: Extra words a user may search by (mode, theatre); shown in the GUI.
    note: str = ""
    #: "map", or what other content this is: "catalog", "models", "gadgets", "cars", ...
    kind: str = "map"


@dataclass
class Input:
    key: str
    label: str
    kind: str = "folder"  # folder | file | files | text | choice
    #: The default value: a callable of the levels folder (so a default may sit under it), or a string.
    default: Callable[[Path], str] | str | None = None
    #: kind "choice": the values offered, as (value, what the window shows).
    choices: list[tuple[str, str]] | None = None
    #: A short hint under the field.
    hint: str = ""


@dataclass
class Task:
    """A run of one of the tool's commands from the GUI (e.g. convert a folder of replays)."""

    id: str
    label: str
    inputs: list[Input]
    #: The command line, from the inputs and the levels folder: `[tool, arg, ...]`.
    argv: Callable[[dict[str, str], Path], list[str]]
    help: str = ""
    #: run: works, then ends (progress, then done) | live: runs until stopped (recording, watching) |
    #: quick: a short command whose output the window shows | open: starts something and returns at once.
    kind: str = "run"
    #: The button's text ("Convert", "Start recording"); a default per kind when empty.
    action: str = ""
    #: The input holding the folder the results go to ("Open output folder"); "" = the levels folder.
    output: str = "out"


@dataclass
class Replays:
    """A replay reader's side of the converter contract: `convert` and `info` (the 3DHeat Library uses both)."""

    game: str
    #: File endings it takes, lower case with the dot (".wrpl").
    extensions: tuple[str, ...]
    #: The tool's own command line that converts one replay into the folder `out`: `[tool, arg, ...]`.
    convert: Callable[[Path, Path], list[str]]
    #: What the replay says about its match, read without converting it where the format allows
    #: (keys as in the contract: map, mode, date, duration_s, players, teams, outcome, game_version); None: not offered.
    info: Callable[[Path], dict] | None = None


@dataclass
class GameSpec:
    key: str
    label: str
    #: The install folder: from a folder the user gave (or None), else found on this machine.
    find: Callable[[str | None], Path | None]
    #: Output folder under the levels folder.
    subdir: str = ""
    #: The game's build/version as the install says it, or None.
    build: Callable[[Path], str | None] | None = None
    #: Map extractors: the maps an install holds.
    maps: Callable[[Path], list[MapSource]] | None = None
    #: Extract one map into `out` (= <levels>/<subdir>); returns the files written. `log` takes text lines.
    extract: Callable[[Path, MapSource, Path, Callable[[str], None]], list[Path]] | None = None
    #: The outputs a map has when it was extracted before manifests existed (for an untracked map).
    existing_outputs: Callable[[Path, MapSource], list[Path]] | None = None
    #: What the tool itself knows about an untracked map or content entry whose outputs exist (extracted
    #: before manifests existed): (install, map, out) -> (extractor version, "current" | "changed"), or
    #: None when it cannot tell. "current" adopts it into the manifest (status writes it then); "changed"
    #: reports it changed. Without a hook or an answer, outputs newer than every source count as current.
    adopt: Callable[[Path, MapSource, Path], tuple[str, str] | None] | None = None
    #: Maps extracted by an extractor older than this are `outdated` (bump when the output changes).
    output_version: str = "0"
    #: Platforms the game exists on (and this tool runs on).
    platforms: tuple[str, ...] = ("windows-x64",)
    #: Non-map content of the install (catalogue, models, gadgets ...): MapSources with kind != "map".
    contents: Callable[[Path], list[MapSource]] | None = None
    #: Extract one content entry into out (= <levels>/<subdir>); returns the files written.
    extract_content: Callable[[Path, MapSource, Path, Callable[[str], None]], list[Path]] | None = None
    #: Item ids the INSTALL holds, by kind ("vehicle", "weapon", "ammo", "gadget", "ship", "car", "operator", ...).
    catalog_items: Callable[[Path], dict[str, list[str]]] | None = None
    #: Item ids already EXTRACTED (default: <out>/catalog.json items[] by "id" and "kind"/"category").
    extracted_items: Callable[[Path], dict[str, list[str]]] | None = None
    #: Where the game's running exe lives, for the "game is running" guard (default: anywhere under the install).
    running: Callable[[Path], bool] | None = None


@dataclass
class Spec:
    id: str
    name: str
    repo: str
    version: str
    #: Command-line tools by their `[project.scripts]` name -> "module:function" (function takes argv).
    tools: dict[str, str]
    default_tool: str
    games: list[GameSpec] = field(default_factory=list)
    #: Extra checks: (found installs by game key, levels folder) -> checks.
    checks: Callable[[dict[str, Path | None], Path], list[Check]] | None = None
    tasks: list[Task] = field(default_factory=list)
    #: Warn when the levels folder has less free space than this.
    min_free_gb: float = 2.0
    description: str = ""
    #: The module that runs this app with `python -m` when not frozen (`<package>.standalone_spec`).
    module: str = ""
    #: A neutral line for the GUI footer (not affiliated ...).
    notice: str = ""
    #: Replay readers: `<id> convert` / `<id> info` (see Replays).
    replays: Replays | None = None
    #: A tool that records in the background: a tray icon while it records (status, Open, Pause, Quit; app/tray.py).
    tray: bool = False

    def has_maps(self) -> bool:
        return any(g.maps is not None and g.extract is not None for g in self.games)

    def has_content(self) -> bool:
        return any(g.contents is not None and g.extract_content is not None for g in self.games)


# ------------------------------------------------------------------ settings


def load_settings(tool_id: str) -> dict:
    try:
        data = json.loads(paths.settings_file(tool_id).read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def save_settings(tool_id: str, data: dict) -> None:
    f = paths.settings_file(tool_id)
    try:
        f.parent.mkdir(parents=True, exist_ok=True)
        tmp = f.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=1), encoding="utf-8")
        tmp.replace(f)
    except OSError:
        pass


def game_folders(spec: Spec, given: dict[str, str] | None = None) -> dict[str, Path | None]:
    """Each game's install: a folder passed now, else the one the user chose in the GUI, else found."""
    chosen = load_settings(spec.id).get("games", {})
    out: dict[str, Path | None] = {}
    for g in spec.games:
        folder = (given or {}).get(g.key) or (chosen.get(g.key) if isinstance(chosen, dict) else None)
        try:
            out[g.key] = g.find(folder)
        except Exception:
            out[g.key] = None
    return out


def standard_checks(spec: Spec, found: dict[str, Path | None], levels: Path) -> list[Check]:
    checks = []
    for g in spec.games:
        p = found.get(g.key)
        checks.append(Check(
            f"game:{g.key}", f"{g.label} install", p is not None,
            str(p) if p else f"Not found on this computer. If {g.label} is installed, choose its folder.",
        ))
    if spec.checks:
        try:
            checks += spec.checks(found, levels)
        except Exception as e:  # a check that breaks is a failed check, not a crash
            checks.append(Check("checks", "Requirements", False, f"{type(e).__name__}: {e}"))
    free = paths.free_bytes(levels)
    need = int(spec.min_free_gb * 1024**3)
    checks.append(Check(
        "disk", "Free disk space", free is None or free >= need,
        "unknown" if free is None else f"{free / 1024**3:.1f} GB free where the maps go"
        + ("" if free >= need else f"; {spec.min_free_gb:g} GB or more advised. Free some space or choose another folder."),
    ))
    return checks
