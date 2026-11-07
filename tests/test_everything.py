"""
Every other property, decoded as far as its bits go; wounds, deaths and
vehicles destroyed from the health the demo replicates; a view's pitch - on
made-up actors.
"""

from __future__ import annotations

import struct

import pytest

from heat3d_ext_squad.bits import BitReader
from heat3d_ext_squad.squad import Match, Player, Sample, decode, is_soldier
from heat3d_ext_squad.stream import Actor, Stats, Vec

from writer import fstring


def bits(data: bytes, n: int | None = None) -> BitReader:
    return BitReader.from_bytes(data, n)


def test_values_are_decoded_as_far_as_their_bits_say():
    assert decode("bHidden", bits(b"\x01", 1)) is True
    assert decode("ServerName", bits(fstring("My server"))) == "My server"
    assert decode("Tickets", bits(struct.pack("<i", 250))) == 250
    assert decode("Health", bits(struct.pack("<f", 37.5))) == 37.5
    assert decode("ReplicatedWorldTimeSecondsDouble", bits(struct.pack("<d", 12.25))) == 12.25
    assert decode("CompressedPing", bits(b"\x0f", 8)) == 15
    # A structure: its bits in hex, and the strings inside it.
    raw = struct.pack("<ii", 2, 1) + struct.pack("<i", 5) + b"BOOM\x00"
    v = decode("#name58", bits(raw + b"\x00", len(raw) * 8 + 3))
    assert v["text"] == ["BOOM"] and v["bits"] == len(raw) * 8 + 3


def _match(props, kind="BP_Soldier_USMC_Rifleman1", name="ann"):
    guid = 10
    actor = Actor(guid=guid, channel=1, opened=0.0, location=Vec(0, 0, 0),
                  path=f"/Game/Blueprints/Soldiers/{kind}.Default__{kind}_C")
    track = [Sample(float(t), 100.0 * t, 0.0, 0.0, 0.0, 0.0) for t in range(20)]
    players = {}
    links = {}
    if name:
        players[1] = Player(1, name=name, pawns=[(0.0, guid)])
        links = {guid: [(0.0, 1)]}
    return Match("m", None, Stats(), players, {}, {}, {guid: actor}, {guid: track}, {}, links, 0, props, {})


def test_a_soldier_wounded_revived_then_killed():
    m = _match({10: {
        "Health": [(1.0, 100.0), (5.0, -0.5), (8.0, 40.0), (12.0, -0.1), (15.0, -300.0)],
        "bWounded": [(5.0, True), (8.0, False), (12.0, True), (15.0, False)],
        "RemoteViewPitch": [(0.0, 127)],
    }})
    got = [(r["time"], r["event"], r["player"], r["x"]) for r in m.casualties()]
    assert got == [(5.0, "wounded", "ann", 500.0), (8.0, "revived", "ann", 800.0), (12.0, "wounded", "ann", 1200.0),
                   (15.0, "death", "ann", 1500.0)]
    pos = [r for r in m.rows() if r["event"] == "position"]
    assert pos[2]["health"] == 100.0 and pos[6]["health"] == -0.5
    assert pos[0]["pitch"] == pytest.approx(127 * 180 / 255 - 90)


def test_a_bot_dies_when_its_health_runs_out():
    assert is_soldier("SQSquidBot")
    m = _match({10: {"Health": [(3.0, 38.0), (4.0, -0.75)]}}, kind="SQSquidBot", name="")
    (death,) = m.casualties()
    assert (death["event"], death["player"], death["time"]) == ("death", "bot 10", 4.0)


def test_a_vehicle_damaged_then_destroyed():
    kind = "BP_M60T_WPMC"
    m = _match({10: {"Health": [(1.0, 2224.0), (2.0, 1448.0), (3.0, -104.0)], "bCanBeDamaged": [(0.0, True)]}},
               kind=kind, name="")
    m.actors[10].path = f"/Game/Vehicles/{kind}.Default__{kind}_C"
    events = [(r["time"], r["event"], r["player"]) for r in m.events()]
    assert events == [(0.0, "spawn", kind), (2.0, "damaged", kind), (3.0, "destroyed", kind)]
    assert [r["health"] for r in m.events()][1:] == [1448.0, -104.0]
