"""
Checks against real Squad server demos, where this machine has them.

The demos are not part of the repository. Point `HEAT3D_SQUAD_DEMOS` at a
folder of `.replay` files to run these; every test is skipped without one.
What is checked holds for any demo, so no names, maps or counts of a
particular match are written here:

- the container and every frame parse, with at most a stray error or two;
- every ReplicatedMovement on a soldier decodes;
- the decoded movement is physically consistent: between two close samples
  the soldier moved about as far as the velocity the sample carries says;
- every row's team is the team whose faction the soldier's blueprint belongs
  to: one team, one set of soldier factions.
"""

from __future__ import annotations

import math
import os
from collections import defaultdict
from pathlib import Path
from statistics import median

import pytest

from heat3d_ext_squad import load
from heat3d_ext_squad.squad import is_soldier

FOLDER = Path(os.environ.get("HEAT3D_SQUAD_DEMOS", "")) if os.environ.get("HEAT3D_SQUAD_DEMOS") else None
DEMOS = sorted(FOLDER.glob("*.replay")) if FOLDER and FOLDER.is_dir() else []

pytestmark = [
    pytest.mark.local,
    pytest.mark.skipif(not DEMOS, reason="no Squad demos on this machine (set HEAT3D_SQUAD_DEMOS)"),
]


@pytest.fixture(scope="module", params=DEMOS, ids=lambda p: f"demo{DEMOS.index(p)}")
def match(request):
    return load(request.param)


def test_container_reads(match):
    r = match.replay
    assert not r.compressed and not r.encrypted
    assert r.header and r.header.levels and r.data_chunks()
    assert r.header.engine_version[0] == 5


def test_stream_has_almost_no_errors(match):
    st = match.stats
    assert st.frames > 1000 and st.packets > st.frames
    assert st.errors <= 2, st.error_samples
    assert match.movement_errors == 0


def test_movement_matches_velocity(match):
    ratios = []
    for guid, track in match.tracks.items():
        if not is_soldier(match.kind(guid)):
            continue
        for a, b in zip(track, track[1:]):
            dt = b.t - a.t
            if 0.05 < dt < 0.3 and b.speed > 150:
                step = math.dist((a.x, a.y), (b.x, b.y))
                ratios.append(step / (b.speed * dt))
    assert len(ratios) > 100
    # Moving players: the step over the time between samples is the speed they report.
    assert 0.8 < median(ratios) < 1.2


def test_teams_match_soldier_factions(match):
    factions = defaultdict(set)
    for r in match.rows():
        if r["event"] == "position" and r["team"] >= 0:
            factions[r["team"]].add(r["pawn"].split("_")[2])  # BP_Soldier_<faction>_...
    assert factions
    for team, seen in factions.items():
        assert len(seen) == 1, (team, seen)
    if len(factions) > 1:
        assert len(set.union(*factions.values())) == len(factions)


def test_rows_are_named(match):
    rows = match.rows()
    assert rows
    assert all(r["player"] for r in rows)
    named = sum(1 for r in rows if not r["player"].startswith(("soldier ", "player ")))
    assert named / len(rows) > 0.9

