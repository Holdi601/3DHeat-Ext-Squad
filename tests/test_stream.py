"""
The network stream and the Squad layer on a synthetic demo: one frame that
exports the names, opens a player state and a soldier, and moves the soldier.
"""

from __future__ import annotations

import json
import struct

import pyarrow.parquet as pq
import pytest

from heat3d_ext_squad import container, output, parse
from heat3d_ext_squad.bits import BitReader
from heat3d_ext_squad.movement import rep_movement as read_movement
from heat3d_ext_squad.stream import Stream

from test_layers import header
from writer import BitWriter, fstring, packed, quantized_vector
from writer import rep_movement as movement_bits

SOLDIER_CLASS = "/Game/Blueprints/Soldiers/X/BP_Soldier_Test.BP_Soldier_Test_C"
SOLDIER_ARCH = "/Game/Blueprints/Soldiers/X/BP_Soldier_Test.Default__BP_Soldier_Test_C"
PS_CLASS = "/Script/Squad.SQPlayerState"
PS_ARCH = "/Script/Squad.Default__SQPlayerState"

GROUPS = {
    SOLDIER_CLASS: ["ReplicatedMovement", "PlayerState"],
    PS_CLASS: ["PlayerNamePrivate", "TeamState", "CurrentPawn"],
}
GUIDS = {20: SOLDIER_ARCH, 22: PS_ARCH}
SOLDIER, PLAYER_STATE = 10, 12


def field_exports() -> bytes:
    out = bytearray()
    entries = []
    for index, (path, names) in enumerate(GROUPS.items()):
        for handle, name in enumerate(names):
            entries.append((index, path if handle == 0 else None, len(names), handle, name))
    out += packed(len(entries))
    for index, path, size, handle, name in entries:
        out += packed(index)
        if path:
            out += packed(1) + fstring(path) + packed(size)
        else:
            out += packed(0)
        out += b"\x01" + packed(handle) + struct.pack("<I", 0) + b"\x00" + fstring(name) + struct.pack("<i", 0)
    return bytes(out)


def guid_exports() -> bytes:
    out = bytearray(packed(len(GUIDS)))
    for guid, path in GUIDS.items():
        body = packed(guid) + b"\x01" + packed(0) + fstring(path)
        out += struct.pack("<i", len(body)) + body
    return bytes(out)


def properties(props: list[tuple[int, BitWriter]]) -> BitWriter:
    w = BitWriter().bit(False)
    for handle, bits in props:
        w.packed(handle + 1).packed(bits.n).append(bits)
    return w.packed(0)


def actor_block(props: list[tuple[int, BitWriter]]) -> BitWriter:
    payload = properties(props)
    return BitWriter().bit(True).bit(True).packed(payload.n).append(payload)


def bunch(ch: int, body: BitWriter, opening: bool) -> BitWriter:
    w = BitWriter()
    w.bit(opening)  # control
    if opening:
        w.bit(True).bit(False)  # open, not close
    w.bit(False)  # replication paused
    w.bit(opening)  # reliable
    w.packed(ch)
    w.bit(False).bit(False).bit(False)  # exports, must-be-mapped, partial
    if opening:
        w.bit(True).packed(102)  # channel name: Actor (hardcoded)
    w.serialized_int(body.n, 1024 * 2 * 8)
    return w.append(body)


def spawn(guid: int, archetype: int, location: tuple[float, float, float] | None) -> BitWriter:
    w = BitWriter().packed(guid).packed(archetype).packed(0)  # level: none
    if location:
        w.bit(True).bit(True)  # serialized, quantized
        quantized_vector(w, location, 10.0)
    else:
        w.bit(False)
    return w.bit(False).bit(False).bit(False)  # rotation, scale, velocity


def name_bits(s: str) -> BitWriter:
    return BitWriter().fstring(s)


def frame(t: float, packets: list[bytes], exports: bool) -> bytes:
    out = struct.pack("<if", 0, t)
    out += field_exports() if exports else packed(0)
    out += guid_exports() if exports else packed(0)
    out += packed(0)  # external data: none
    out += packed(0)  # streaming levels: none
    for p in packets:
        out += struct.pack("<i", len(p)) + p
    return out + struct.pack("<i", 0)


def synthetic_demo() -> bytes:
    ps_open = spawn(PLAYER_STATE, 22, None).append(actor_block([
        (0, name_bits("Tester")), (2, BitWriter().packed(SOLDIER)),
    ]))
    soldier_open = spawn(SOLDIER, 20, (100.0, 200.0, 30.0)).append(actor_block([
        (1, BitWriter().packed(PLAYER_STATE)),
        (0, movement_bits((100.0, 200.0, 30.0), 64)),
    ]))
    first = frame(1.0, [bunch(3, ps_open, True).packet(), bunch(4, soldier_open, True).packet()], True)
    frames = [first]
    for i in range(1, 5):
        pos = (100.0 + 50 * i, 200.0 - 25.5 * i, 30.0)
        frames.append(frame(1.0 + 0.125 * i, [bunch(4, actor_block([(0, movement_bits(pos, 64, (400, -204, 0)))]),
                                                     False).packet()], False))
    return container.build(header(), [(0, 2000, b"".join(frames))], length_ms=2000)


def test_movement_round_trip():
    w = movement_bits((-1234.56, 789.01, -42.5), 192, (300, -150, 5))
    m = read_movement(BitReader(w.value, w.n), 36)
    assert (round(m.location.x, 2), round(m.location.y, 2), round(m.location.z, 2)) == (-1234.56, 789.01, -42.5)
    assert m.yaw == pytest.approx(-90.0)
    assert (m.velocity.x, m.velocity.y, m.velocity.z) == (300, -150, 5)


def test_movement_with_stray_bits_is_refused():
    w = movement_bits((1.0, 2.0, 3.0), 0).bits(0b11, 2)
    with pytest.raises(ValueError):
        read_movement(BitReader(w.value, w.n), 36)


def test_stream_reports_actors_and_properties():
    buf = synthetic_demo()
    seen = []
    s = Stream(container.read(buf), buf, on_property=lambda t, a, g, o, n, b: seen.append((a.guid, g.path, n)))
    st = s.run()
    assert st.errors == 0, st.error_samples
    assert (st.frames, st.packets, st.actor_opens) == (5, 6, 2)
    assert s.actors[SOLDIER].path == SOLDIER_ARCH
    assert (s.actors[SOLDIER].location.x, s.actors[SOLDIER].location.y) == (100.0, 200.0)
    assert (PLAYER_STATE, PS_CLASS, "PlayerNamePrivate") in seen
    assert sum(1 for g, _, n in seen if g == SOLDIER and n == "ReplicatedMovement") == 5


def test_squad_layer_names_the_track(tmp_path):
    m = parse(synthetic_demo(), "synthetic")
    rows = m.rows()
    assert len(rows) == 5
    assert {r["player"] for r in rows} == {"Tester"}
    assert rows[0]["pawn"] == "BP_Soldier_Test" and rows[0]["event"] == "position"
    assert (rows[-1]["x"], rows[-1]["y"]) == pytest.approx((300.0, 98.0))
    assert rows[0]["yaw"] == pytest.approx(90.0)
    data, doc = output.write(m, tmp_path)
    t = pq.read_table(data)
    hints = json.loads(t.schema.metadata[b"heat3d"])
    assert hints["axes"]["up"] == "z" and hints["columns"]["personId"] == "player"
    assert t.num_rows == 5 and set(t.column("player").to_pylist()) == {"Tester"}
    summary = json.loads(doc.read_text(encoding="utf-8"))
    assert summary["layer"] == "Test_Layer_v1" and summary["map"] == "Test_Map"
    assert summary["players"][0]["name"] == "Tester" and summary["players"][0]["on_foot_samples"] == 5
