"""
3DHeat Squad demo reader: Squad server demos (Unreal network replays) into
heatmap tables - every player's position, team and squad over the match.

    from heat3d_ext_squad import load, write
    match = load("match.replay")
    write(match, "out")

The layers: `container` (the file and its chunks), `bits` (byte and bit
archives), `stream` (frames, packets, bunches, actors, properties), `movement`
(the engine's FRepMovement), `squad` (which Squad classes say what), `output`
(Parquet and match JSON), `cli`.
"""

__version__ = "0.1.0"

from .output import write  # noqa: E402
from .squad import Match, load, parse  # noqa: E402

__all__ = ["Match", "load", "parse", "write", "__version__"]
