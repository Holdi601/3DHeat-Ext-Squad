"""
Everything a demo holds is decoded, or kept whole in a sidecar, or both - on
a synthetic demo that holds one of every kind of item the reader meets: the
container's chunks, export tables, actors opened and closed, properties
named and unnamed, remote calls, a component the exports name only by the
frame its fields were first sent in, a component no export names, a bunch
on a channel opened before the recording, the tail of a partial bunch, and
a packet that does not read.
"""

from __future__ import annotations

import json
import math
import struct

import pyarrow.parquet as pq
import pytest

from heat3d_ext_squad import container, output, parse
from heat3d_ext_squad.bits import BitReader
from heat3d_ext_squad.keep import RULE
from heat3d_ext_squad.movement import helicopter_movement as read_heli

from test_layers import header
from test_stream import bunch, name_bits, spawn
from writer import BitWriter, fstring, helicopter_movement, packed
from writer import rep_movement as movement_bits

SOLDIER_CLASS = "/Game/Blueprints/Soldiers/X/BP_Soldier_Test.BP_Soldier_Test_C"
PS_CLASS = "/Script/Squad.SQPlayerState"
GUN_CLASS = "/Game/Weapons/BP_Gun.BP_Gun_C"
FIRE = "/Script/Squad.SQWeapon:MulticastFireProjectile"
HELI_CLASS = "/Game/Vehicles/BP_Heli.BP_Heli_C"
HELI_MOVE = "/Script/Squad.SQHelicopterMovementComponent"

#: (index, path, size, {handle: name}); the helicopter's movement component is exported in a later frame.
FIRST = [
    (0, SOLDIER_CLASS, 2, {0: "ReplicatedMovement", 1: "PlayerState"}),
    (1, PS_CLASS, 3, {0: "PlayerNamePrivate", 1: "TeamState", 2: "CurrentPawn"}),
    (2, GUN_CLASS, 1, {0: "Owner"}),
    (3, GUN_CLASS + "_ClassNetCache", 3, {0: "MulticastFireProjectile", 1: "MulticastStopFire"}),
    (4, FIRE, 2, {0: "OriginZeroBased", 1: "ShootDir"}),
    (5, HELI_CLASS, 1, {0: "bHidden"}),
]
SECOND = [(6, HELI_MOVE, 5, {2: "ReplicatedMovement", 3: "bIsSimulatingPhysics"})]
GUIDS = {20: "/Game/Blueprints/Soldiers/X/BP_Soldier_Test.Default__BP_Soldier_Test_C",
         22: "/Script/Squad.Default__SQPlayerState", 24: "/Game/Weapons/BP_Gun.Default__BP_Gun_C",
         26: "/Game/Vehicles/BP_Heli.Default__BP_Heli_C", 31: "MovementComponent", 33: "Mystery"}
SOLDIER, PLAYER_STATE, GUN, HELI = 10, 12, 14, 16


def exports(groups) -> bytes:
    out = bytearray()
    entries = []
    for index, path, size, fields in groups:
        for i, (handle, name) in enumerate(sorted(fields.items())):
            entries.append((index, path if i == 0 else None, size, handle, name))
    out += packed(len(entries))
    for index, path, size, handle, name in entries:
        out += packed(index)
        out += packed(1) + fstring(path) + packed(size) if path else packed(0)
        out += b"\x01" + packed(handle) + struct.pack("<I", 7) + b"\x00" + fstring(name) + struct.pack("<i", 0)
    return bytes(out)


def guid_exports() -> bytes:
    out = bytearray(packed(len(GUIDS)))
    for guid, path in GUIDS.items():
        body = packed(guid) + b"\x01" + packed(0) + fstring(path)
        out += struct.pack("<i", len(body)) + body
    return bytes(out)


def props(items: list[tuple[int, BitWriter]]) -> BitWriter:
    w = BitWriter().bit(False)
    for handle, bits in items:
        w.packed(handle + 1).packed(bits.n).append(bits)
    return w.packed(0)


def block(payload: BitWriter, obj: int | None = None) -> BitWriter:
    """A content block: for the actor itself, or for a stably named subobject `obj`."""
    w = BitWriter().bit(True)
    if obj is None:
        w.bit(True)
    else:
        w.bit(False).packed(obj).bit(True)
    return w.packed(payload.n).append(payload)


def fire_call() -> BitWriter:
    """MulticastFireProjectile with its two parameters, after the gun's (empty) property list."""
    params = BitWriter().bit(False)
    origin = BitWriter().f64(1000.0).f64(-2000.0).f64(150.0)
    direction = BitWriter()
    for c in (1.0, 0.0, 0.0):
        direction.bits(round(c * 32767) + 32768, 16)
    params.packed(1).packed(origin.n).append(origin).packed(2).packed(direction.n).append(direction).packed(0)
    w = BitWriter().bit(False).packed(0)  # properties: none
    w.serialized_int(0, 3).packed(params.n).append(params)  # field 0 of the class net cache
    w.serialized_int(1, 3).packed(0)  # MulticastStopFire: no parameters
    return w


def partial_tail(ch: int, body: BitWriter) -> BitWriter:
    """The last part of a partial bunch whose first part the recording never had."""
    w = BitWriter().bit(False)  # not control
    w.bit(False).bit(False).packed(ch)  # paused, reliable, channel
    w.bit(False).bit(False)  # exports, must-be-mapped
    w.bit(True).bit(False).bit(False).bit(True)  # partial, not initial, custom exports final, final
    w.serialized_int(body.n, 1024 * 2 * 8)
    return w.append(body)


def frame(t: float, packets: list[bytes], field_exports: bytes = b"", guids: bytes = b"") -> bytes:
    out = struct.pack("<if", 0, t) + (field_exports or packed(0)) + (guids or packed(0))
    out += packed(0) + packed(0)  # no external data, no streaming levels
    for p in packets:
        out += struct.pack("<i", len(p)) + p
    return out + struct.pack("<i", 0)


def demo() -> bytes:
    ps = spawn(PLAYER_STATE, 22, None).append(block(props([(0, name_bits("Tester")), (2, BitWriter().packed(SOLDIER))])))
    soldier = spawn(SOLDIER, 20, (100.0, 200.0, 30.0)).append(block(props([
        (1, BitWriter().packed(PLAYER_STATE)), (0, movement_bits((100.0, 200.0, 30.0), 64))])))
    gun = spawn(GUN, 24, (100.0, 200.0, 30.0)).append(block(props([(0, BitWriter().packed(SOLDIER))])))
    heli = spawn(HELI, 26, (5000.0, 6000.0, 10.0)).append(block(props([(0, BitWriter().bit(False))])))
    frames = [frame(1.0, [bunch(3, ps, True).packet(), bunch(4, soldier, True).packet(), bunch(5, gun, True).packet(),
                          bunch(6, heli, True).packet()], exports(FIRST), guid_exports())]
    # The helicopter's component: its class's fields are exported in the frame it first sends them.
    move = block(props([(2, helicopter_movement((5000.0, 6000.0, 10.0), 90.0, (0.0, 0.0, 0.0), 100.0))]), obj=31)
    frames.append(frame(1.125, [bunch(6, move, False).packet()], exports(SECOND)))
    frames.append(frame(1.25, [
        bunch(5, block(fire_call()), False).packet(),
        bunch(6, block(props([(2, helicopter_movement((5100.0, 6000.0, 10.0), 90.0, (800.0, 0.0, 0.0), 100.125))]),
                       obj=31), False).packet(),
        bunch(6, block(props([(0, BitWriter().bit(True))]), obj=33), False).packet(),  # no export names "Mystery"
        bunch(4, block(props([(5, BitWriter().bits(3, 3))])), False).packet(),  # a handle the exports never named
        bunch(40, BitWriter().bits(0x2A5, 11), False).packet(),  # a channel opened before the recording
        partial_tail(41, BitWriter().bits(0x15, 7)).packet(),
        b"\x00\x00",  # no end marker: not a packet that reads
    ]))
    return container.build(header(), [(0, 2000, b"".join(frames))], [("ev1", "kills", "meta", 1100, 1200, b"payload")],
                           length_ms=2000)


@pytest.fixture(scope="module")
def match():
    return parse(demo(), "synthetic")


def test_nothing_is_lost(match):
    c = match.keeper.completeness([])
    assert c["lost"] == 0, {k: v for k, v in c["types"].items() if v["lost"]}
    types = c["types"]
    for kind in ("file.info", "chunk.header", "chunk.replayData", "chunk.event", "frame", "packet", "bunch", "open",
                 "export.field", "export.guid", "property:BP_Soldier_Test_C", "property:SQPlayerState",
                 "rpc:BP_Gun_C", "property:SQHelicopterMovementComponent", "block:Mystery"):
        assert types[kind]["seen"] > 0, kind
    assert types["chunk.event"]["raw"] == 1
    assert types["packet"]["raw"] == 1  # the one that does not read, kept whole
    assert types["block:Mystery"]["raw"] == 1
    assert types["property:BP_Soldier_Test_C"]["raw"] == 1  # the unnamed handle
    assert types["rpc:BP_Gun_C"] == {"seen": 2, "decoded": 0, "partial": 2, "raw": 0, "lost": 0}


def test_a_component_is_named_by_the_frame_its_fields_were_exported_in(match):
    g, how, blocks = match.stream.resolution[("BP_Heli_C", "MovementComponent")]
    assert (g.path, how, blocks) == (HELI_MOVE, "export frame", 2)
    assert match.stream.resolution[("BP_Heli_C", "Mystery")][0] is None
    track = match.tracks[HELI]
    assert [(s.t, s.x, s.y) for s in track] == [(1.125, 5000.0, 6000.0), (1.25, 5100.0, 6000.0)]
    assert track[0].yaw == pytest.approx(90.0, abs=0.01) and track[1].speed == pytest.approx(800.0)


def test_helicopter_movement_round_trip():
    w = helicopter_movement((-1234.56, 789.01, 42.5), 271.0, (300.0, -150.25, 5.0), 54764.33)
    m, clock = read_heli(BitReader(w.value, w.n))
    assert (round(m.location.x, 2), round(m.location.y, 2), round(m.location.z, 2)) == (-1234.56, 789.01, 42.5)
    assert m.yaw == pytest.approx(-89.0, abs=0.01)
    assert (m.velocity.x, m.velocity.y) == pytest.approx((300.0, -150.25))
    assert clock == pytest.approx(54764.33, abs=0.01)


def test_shots_come_from_the_weapons_calls(match):
    (shot,) = match.shots
    assert (shot.function, shot.origin, shot.direction) == ("MulticastFireProjectile", (1000.0, -2000.0, 150.0),
                                                            (1.0, 0.0, 0.0))
    rows = [r for r in match.rows() if r["event"] == "fire"]
    assert len(rows) == 1 and rows[0]["player"] == "Tester" and rows[0]["pawn"] == "BP_Gun"
    assert rows[0]["entity"] == GUN and rows[0]["yaw"] == pytest.approx(0.0)


def test_sidecars_hold_every_item_whole(match, tmp_path):
    data, doc = output.write(match, tmp_path)
    summary = json.loads(doc.read_text(encoding="utf-8"))
    check = summary["selfCheck"]["completeness"]
    assert check["rule"] == RULE and check["lost"] == 0
    assert check["sidecars"] == ["synthetic.entities.parquet", "synthetic.packets.parquet"]
    ent = pq.read_table(tmp_path / "synthetic.entities.parquet").to_pylist()
    pkt = pq.read_table(tmp_path / "synthetic.packets.parquet").to_pylist()
    assert list(pq.read_schema(tmp_path / "synthetic.entities.parquet").names[:4]) == ["time", "type", "name", "entity"]
    # The event chunk, whole.
    (ev,) = [r for r in pkt if r["type"] == "chunk.event"]
    raw = demo()
    assert ev["payload"] == raw[ev["offset"] : ev["offset"] + len(ev["payload"])]
    assert json.loads(ev["decoded"])["id"] == "ev1"
    # The bunch on a channel the recording never opened, and the orphan tail: their bits, with their count.
    (unopened,) = [r for r in pkt if r["type"] == "bunch.unopened"]
    assert (unopened["bits"], unopened["payload"]) == (11, (0x2A5).to_bytes(2, "little"))
    (orphan,) = [r for r in pkt if r["type"] == "bunch.orphan"]
    assert (orphan["bits"], orphan["payload"]) == (7, b"\x15")
    # Every property row joins to an actor; the one no export names keeps its bits.
    (mystery,) = [r for r in ent if r["kind"] == "block"]
    assert mystery["entity"] == HELI and mystery["type"] == "Mystery"
    names = {r["type"] for r in ent if r["kind"] == "property"}
    assert {"SQPlayerState.PlayerNamePrivate", "BP_Soldier_Test_C.#5", "SQHelicopterMovementComponent.ReplicatedMovement"} <= names
    call = [r for r in ent if r["type"] == "BP_Gun_C.MulticastFireProjectile"][0]
    assert json.loads(call["decoded"])["ShootDir"] == [1.0, 0.0, 0.0]
    # The context a later reader needs: every export, in the sidecar itself.
    fields = {(json.loads(r["decoded"])["group"], r["handle"]) for r in ent if r["kind"] == "export.field"}
    assert (HELI_MOVE, 2) in fields and (FIRE, 1) in fields
    assert {r["entity"] for r in ent if r["kind"] == "export.guid"} >= set(GUIDS)
    t = pq.read_table(data)
    assert "entity" in t.column_names and "detail" in t.column_names
    assert summary["stream"]["class_resolution"]["keys"] == {"export frame": 1, "unresolved": 1}


def test_parse_without_keeping_writes_no_sidecars(tmp_path):
    m = parse(demo(), "plain", keep=False)
    output.write(m, tmp_path)
    assert sorted(p.name for p in tmp_path.iterdir()) == ["plain.match.json", "plain.parquet"]
    assert math.isfinite(m.tracks[HELI][0].x)
