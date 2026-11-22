"""
What a Squad server demo says about its match, from the replay's info block
and demo header only: the frames are not read.

The info block gives the recording's length, its friendly name and when it
was recorded; the demo header (`container.read_header`) the level - the
layer's path, `/Game/Maps/<Map>/Gameplay_Layers/<Layer>` - and the game's
build. Who played and on which team, and how the match ended, are only in the
replicated stream, so `players`, `teams` and `outcome` stay empty here.

The file is mapped rather than read: walking the chunk table touches only the
few bytes of each chunk's own header, so a long demo costs no more than a short one.
"""

from __future__ import annotations

import mmap
import re
from datetime import datetime, timedelta
from pathlib import Path

from . import container
from .bits import ReadError
from .cli import map_folder


def _date(ticks_unix: float | None) -> str | None:
    """When the demo was recorded. The file gives the clock reading without its zone, so the time is naive."""
    if ticks_unix is None:
        return None
    try:
        return (datetime(1970, 1, 1) + timedelta(seconds=ticks_unix)).isoformat(timespec="seconds")
    except OverflowError:
        return None


def _mode(layer: str) -> str | None:
    """The mode in a layer named `<Map>_<Mode>_v<N>` (e.g. `..._AAS_v1`); None for a name not so made."""
    parts = layer.split("_")
    if len(parts) >= 3 and re.fullmatch(r"v\d+", parts[-1], re.IGNORECASE) and parts[-2].isalpha():
        return parts[-2]
    return None


def info(path: Path) -> dict:
    """The match a Squad demo holds: map, layer, mode, date, length and game version (no roster: see above)."""
    path = Path(path)
    with open(path, "rb") as f:
        if path.stat().st_size < 8:
            raise ValueError("not a Squad demo: the file is too short")
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as buf:
            try:
                r = container.read(buf)
            except (ReadError, ValueError) as e:
                raise ValueError(f"not a Squad demo: {e}") from e
    h = r.header
    if h is None:
        raise ValueError("not a Squad demo: the replay has no demo header")
    level = h.levels[0][0] if h.levels else ""
    if "Gameplay_Layers" not in level and "squad" not in h.branch.lower():
        raise ValueError("not a Squad demo: an Unreal replay of another game")
    layer = level.rsplit("/", 1)[-1] if level else None
    return {
        "map": map_folder(level) if level else None,
        "map_title": None,
        "layer": layer,
        "level_path": level or None,
        "mode": _mode(layer) if layer else None,
        "date": _date(r.recorded_unix),
        "duration_s": round(r.length_ms / 1000.0, 3) if r.length_ms else None,
        "players": [],
        "teams": [],
        "outcome": None,
        "game_version": (h.branch.rsplit("/", 1)[-1] or None) if h.branch else None,
        "engine_version": ".".join(str(v) for v in h.engine_version) if any(h.engine_version) else None,
        "recording_name": r.friendly_name or None,
        "platform": h.platform or None,
    }
