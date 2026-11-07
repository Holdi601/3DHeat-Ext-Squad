"""
The replay's network stream: frames, packets, bunches, channels, actors and
their replicated properties.

Each replay data chunk is a run of frames. A frame is a byte archive:

    [level index]  time  net field exports  exported net GUIDs
    [streaming levels]  external data  [game frame data]  packets...

and each packet is a bit stream of bunches - the same bunches a server sends a
client, recorded by the server's demo driver. A bunch belongs to a channel; an
actor channel's first bunch opens the actor (its net GUID, archetype, level,
and where it spawned), and every bunch after carries content blocks: for the
actor or one of its subobjects, a list of (property handle, bit count, bits).

What makes a replay readable without the game's code is that the demo driver
writes the *names* too: the net field export groups map each class path and
property handle to the property's name, and the exported net GUIDs map object
ids to paths. Every property's bits can be found by name; decoding the bits
still needs the property's type, which this module leaves to its caller
(`movement.py` for the engine's own FRepMovement, `squad.py` for the rest).

The layout is the engine's, as generic readers document it (Unreal.Core in
FortniteReplayDecompressor, MIT); the version checks are against
EEngineNetworkVersionHistory, and the whole path was checked on real Squad
v10.3.1 server demos (engine network version 36).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterator

from .bits import BitReader, ByteReader, ReadError, concat
from .container import DemoHeader, ReplayFile

# EEngineNetworkVersionHistory steps that change what is read.
ENG_CHANNEL_INDEX_PACKED = 3
ENG_LEVEL_IN_SPAWN = 5
ENG_CHANNEL_NAMES = 6
ENG_CHANNEL_CLOSE_REASON = 7
ENG_NO_EXTRA_BUNCH_BIT = 8
ENG_FNAME_EXPORTS = 10
ENG_OPTIONAL_QUANTIZE = 13
ENG_SUBOBJECT_OUTER = 18
ENG_DOUBLE_VECTORS = 23
ENG_REP_MOVE_SERVER_FRAME = 25
ENG_SUBOBJECT_DESTROY_FLAG = 30
#: Partial bunches carry a third flag, "custom exports final", between initial
#: and final. Present at 36 (Squad v10.3.1); the step that added it is not
#: pinned down, so older versions are read without it.
ENG_PARTIAL_CUSTOM_EXPORTS = 36

#: The largest bunch a demo connection writes, in bits (MAX_DEMO_READ_WRITE_BUFFER * 8).
MAX_BUNCH_BITS = 1024 * 2 * 8


@dataclass
class Vec:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0


@dataclass
class Actor:
    guid: int
    channel: int
    opened: float
    archetype: int | None = None
    level: int | None = None
    location: Vec | None = None
    rotation: tuple[float, float, float] | None = None
    path: str = ""  # the archetype's path, when the stream exported it
    closed: float | None = None


@dataclass
class Group:
    path: str
    size: int
    fields: dict[int, str] = field(default_factory=dict)


@dataclass
class Stats:
    frames: int = 0
    packets: int = 0
    bunches: int = 0
    actor_opens: int = 0
    content_blocks: int = 0
    unresolved_blocks: int = 0
    properties: int = 0
    external: int = 0
    errors: int = 0
    error_samples: list[str] = field(default_factory=list)

    def error(self, where: str, e: Exception) -> None:
        self.errors += 1
        if len(self.error_samples) < 20:
            self.error_samples.append(f"{where}: {e}")


#: on_property(time, actor or None, group, object guid, property name, bits)
PropertySink = Callable[[float, "Actor | None", Group, int, str, BitReader], None]


class Stream:
    """
    Reads every data chunk of a replay and reports actors and properties.

    `on_open(actor)`, `on_close(actor)` and `on_property(...)` are called as
    the stream goes; `on_property` only for the property names in `wanted`
    (all of them when `wanted` is None), so the bits nobody asked for are
    skipped, not decoded.
    """

    def __init__(self, replay: ReplayFile, buf: bytes, *, wanted: set[str] | None = None,
                 on_open: Callable[[Actor], None] | None = None,
                 on_close: Callable[[Actor], None] | None = None,
                 on_property: PropertySink | None = None):
        if replay.header is None:
            raise ReadError("the replay has no header chunk")
        if replay.compressed or replay.encrypted:
            raise ReadError("compressed or encrypted replay data is not read")
        self.replay = replay
        self.buf = buf
        self.h: DemoHeader = replay.header
        self.eng = self.h.engine_network_version
        self.wanted = wanted
        self.on_open = on_open
        self.on_close = on_close
        self.on_property = on_property
        self.stats = Stats()
        self.guid_paths: dict[int, str] = {}
        self.groups: dict[str, Group] = {}
        self.group_by_index: dict[int, Group] = {}
        self._by_leaf: dict[str, Group] = {}
        self._resolved: dict[str, Group | None] = {}
        self.channels: dict[int, Actor] = {}
        self.actors: dict[int, Actor] = {}
        self._partial: dict[int, tuple[int, int]] = {}  # channel -> (bits, count)
        self._partial_open: dict[int, bool] = {}
        self.time = 0.0

    # ------------------------------------------------------------- frames

    def run(self) -> Stats:
        for c in self.replay.data_chunks():
            r = ByteReader(self.buf, c.data_offset, c.data_offset + c.data_size)
            while r.left() > 0:
                try:
                    self._frame(r)
                except ReadError as e:
                    # A frame that does not parse leaves the reader nowhere
                    # trustworthy in this chunk; go on with the next one.
                    self.stats.error(f"frame at byte {r.pos}", e)
                    break
        return self.stats

    def _frame(self, r: ByteReader) -> None:
        self.stats.frames += 1
        if self.h.network_version >= 6:
            r.i32()  # the current level's index
        self.time = r.f32()
        if self.h.network_version >= 10:
            self._field_exports(r)
            self._guid_exports(r)
        if self.h.streaming_fixes:
            for _ in range(r.packed()):
                r.fstring()
            r.u64()  # the offset of the external data, for seeking
            self._external(r)
        else:
            self._external(r)
            # In the layout without streaming fixes a (normally empty) list of
            # streaming level names follows the external data.
            for _ in range(r.packed()):
                r.fstring()
        if self.h.game_specific_frame_data:
            n = r.u64()
            r.skip(n)
        while True:
            if self.h.streaming_fixes:
                r.packed()  # the level the packet was seen in
            size = r.i32()
            if size <= 0:
                return  # 0 ends the frame's packets (a negative size marks the end of a checkpoint)
            data = r.bytes(size)
            self.stats.packets += 1
            try:
                self._packet(data)
            except ReadError as e:
                self.stats.error(f"packet at {self.time:.2f}s", e)

    def _field_exports(self, r: ByteReader) -> None:
        for _ in range(r.packed()):
            index = r.packed()
            if r.packed():
                path = r.fstring()
                size = r.packed()
                g = self.groups.get(path)
                if g is None:
                    g = self.groups[path] = Group(path, size)
                    self._by_leaf.setdefault(_leaf(path), g)
                    self._resolved.clear()
                self.group_by_index[index] = g
            g = self.group_by_index.get(index)
            if r.u8():
                handle = r.packed()
                r.u32()  # the property's compatibility checksum
                if self.eng < ENG_FNAME_EXPORTS:
                    name = r.fstring()
                else:
                    hardcoded = r.u8()
                    if hardcoded:
                        name = f"#name{r.packed()}"
                    else:
                        name = r.fstring()
                        r.i32()  # the FName's number
                if g is not None:
                    g.fields[handle] = name

    def _guid_exports(self, r: ByteReader) -> None:
        for _ in range(r.packed()):
            size = r.i32()
            data = r.bytes(size)
            try:
                self._net_guid(BitReader.from_bytes(data), exporting=True)
            except ReadError as e:
                self.stats.error("exported net GUID", e)

    def _external(self, r: ByteReader) -> None:
        # Properties some actors hand the demo driver outside their bunches.
        while True:
            bits = r.packed()
            if bits == 0:
                return
            r.packed()  # the actor's net GUID
            r.skip((bits + 7) // 8)
            self.stats.external += 1

    # ------------------------------------------------------------- packets

    def _packet(self, data: bytes) -> None:
        if not data or data[-1] == 0:
            raise ReadError("packet without its end marker")
        # The last set bit is the end marker; the bunches are what comes before it.
        bits = len(data) * 8 - 1 - (8 - data[-1].bit_length())
        p = BitReader.from_bytes(data, bits)
        while not p.at_end():
            self._bunch(p)

    def _bunch(self, p: BitReader) -> None:
        eng = self.eng
        if eng < ENG_NO_EXTRA_BUNCH_BIT:
            p.bit()
        control = p.bit()
        opening = control and p.bit()
        closing = control and p.bit()
        if closing:
            if eng < ENG_CHANNEL_CLOSE_REASON:
                p.bit()
            else:
                p.serialized_int(15)
        p.bit()  # replication paused
        reliable = p.bit()
        ch = p.packed() if eng >= ENG_CHANNEL_INDEX_PACKED else p.serialized_int(1 << 32)
        has_exports = p.bit()
        p.bit()  # has must-be-mapped GUIDs
        partial = p.bit()
        partial_initial = partial and p.bit()
        if partial and eng >= ENG_PARTIAL_CUSTOM_EXPORTS:
            p.bit()  # custom exports final
        partial_final = partial and p.bit()
        if eng >= ENG_CHANNEL_NAMES and (reliable or opening):
            p.fname()  # the channel's kind: Actor, Control, Voice
        n = p.serialized_int(MAX_BUNCH_BITS)
        body = p.window(n)
        self.stats.bunches += 1
        if has_exports:
            if body.bit():
                raise ReadError("rep layout exports inside a bunch")
            count = body.i32()
            if count < 0 or count > 2048:
                raise ReadError(f"{count} GUIDs exported in a bunch")
            for _ in range(count):
                self._net_guid(body, exporting=True)
        if partial:
            if partial_initial:
                self._partial[ch] = body.rest()
                self._partial_open[ch] = opening
                if not partial_final:
                    return
            elif ch in self._partial:
                if not has_exports:
                    self._partial[ch] = concat(self._partial[ch], body.rest())
                if not partial_final:
                    return
            else:
                return  # the rest of a bunch whose start was not recorded
            value, count = self._partial.pop(ch)
            opening = self._partial_open.pop(ch, opening)
            body = BitReader(value, count)
        try:
            self._channel_bunch(ch, opening, closing, body)
        except ReadError as e:
            self.stats.error(f"channel {ch} at {self.time:.2f}s", e)
        if closing:
            actor = self.channels.pop(ch, None)
            if actor is not None:
                actor.closed = self.time
                if self.on_close:
                    self.on_close(actor)

    # ------------------------------------------------------------- objects

    def _net_guid(self, r: BitReader, exporting: bool, depth: int = 0) -> int:
        """A net GUID; when it is exported (or the default), its outer and path follow."""
        if depth > 16:
            raise ReadError("net GUID outers nested too deep")
        guid = r.packed()
        if guid == 0:
            return 0
        if guid == 1 or exporting:
            flags = r.u8()
            if flags & 1:  # has path
                self._net_guid(r, True, depth + 1)
                path = r.fstring()
                if flags & 4:  # has network checksum
                    r.u32()
                if exporting:
                    self.guid_paths[guid] = path
        return guid

    def _channel_bunch(self, ch: int, opening: bool, closing: bool, b: BitReader) -> None:
        actor = self.channels.get(ch)
        if actor is None:
            if not opening or b.at_end():
                return  # a channel opened before the recording, or only being closed
            actor = self._spawn(ch, b)
        while not b.at_end():
            self._content_block(actor, b)

    def _spawn(self, ch: int, b: BitReader) -> Actor:
        a = Actor(guid=self._net_guid(b, False), channel=ch, opened=self.time)
        if a.guid and not a.guid & 1 and not b.at_end():  # dynamic: spawned, so its spawn info follows
            a.archetype = self._net_guid(b, False)
            if self.eng >= ENG_LEVEL_IN_SPAWN:
                a.level = self._net_guid(b, False)
            a.location = self._optional_vector(b, Vec())
            if b.bit():
                a.rotation = tuple(b.u16() * 360.0 / 65536.0 if b.bit() else 0.0 for _ in range(3))
            self._optional_vector(b, Vec(1, 1, 1))  # scale
            self._optional_vector(b, Vec())  # velocity
            a.path = self.guid_paths.get(a.archetype, "")
        else:
            a.path = self.guid_paths.get(a.guid, "")
        self.channels[ch] = a
        self.actors[a.guid] = a
        self.stats.actor_opens += 1
        if self.on_open:
            self.on_open(a)
        return a

    def _optional_vector(self, b: BitReader, default: Vec) -> Vec:
        if not b.bit():
            return default
        if self.eng < ENG_OPTIONAL_QUANTIZE or b.bit():
            return packed_vector(b, 10.0, 24, self.eng)
        if self.eng >= ENG_DOUBLE_VECTORS:
            return Vec(b.f64(), b.f64(), b.f64())
        return Vec(b.f32(), b.f32(), b.f32())

    def _content_block(self, actor: Actor, b: BitReader) -> None:
        self.stats.content_blocks += 1
        has_rep_layout = b.bit()
        if b.bit():  # the actor itself
            obj = actor.guid
            path = actor.path
        else:
            obj = self._net_guid(b, False)
            if b.bit():  # stably named: its path is known from the exports
                path = self.guid_paths.get(obj, "")
            else:
                if self.eng >= ENG_SUBOBJECT_DESTROY_FLAG and b.bit():
                    b.u8()  # destroy flags
                    return
                cls = self._net_guid(b, False)
                if cls == 0:
                    return  # the subobject was deleted
                if self.eng >= ENG_SUBOBJECT_OUTER and not b.bit():
                    self._net_guid(b, False)  # its outer, when it is not the actor
                path = self.guid_paths.get(cls, "")
        n = b.packed()
        payload = b.window(n)
        if not has_rep_layout or n == 0:
            return  # RPCs and custom-delta structures; not read
        g = self.group_for(path)
        if g is None:
            self.stats.unresolved_blocks += 1
            return
        self._properties(actor, g, obj, payload)

    def group_for(self, path: str) -> Group | None:
        """The net field export group of an object path: an archetype, a class, a stably named subobject."""
        if not path:
            return None
        if path in self._resolved:
            return self._resolved[path]
        g = self.groups.get(path)
        if g is None:
            leaf = _leaf(path)
            g = self._by_leaf.get(leaf) or self._by_leaf.get(leaf + "_C")
        self._resolved[path] = g
        return g

    def _properties(self, actor: Actor, g: Group, obj: int, b: BitReader) -> None:
        b.bit()  # the checksum flag of the backwards-compatible layout
        while not b.at_end():
            handle = b.packed()
            if handle == 0:
                return
            handle -= 1
            n = b.packed()
            bits = b.window(n)
            name = g.fields.get(handle)
            if name is None:
                continue
            self.stats.properties += 1
            if self.on_property and (self.wanted is None or name in self.wanted):
                self.on_property(self.time, actor, g, obj, name, bits)


def _leaf(path: str) -> str:
    """`/Game/X/BP_Soldier.Default__BP_Soldier_C` and `/Game/X/BP_Soldier.BP_Soldier_C` both become `BP_Soldier_C`."""
    leaf = path.rsplit(":", 1)[-1] if ":" in path else path
    leaf = leaf.rsplit(".", 1)[-1].rsplit("/", 1)[-1]
    if leaf.startswith("Default__"):
        leaf = leaf[len("Default__"):]
    if leaf.endswith("_ClassNetCache"):
        leaf = leaf[: -len("_ClassNetCache")]
    return leaf


def packed_vector(b: BitReader, scale: float, max_bits: int, eng: int) -> Vec:
    """
    A quantized vector (WritePackedVector / WriteQuantizedVector).

    From engine network version 23 (large world coordinates) a 7-bit header
    gives the bits per component and whether the values are scaled; with 0
    bits the components are plain floats or doubles. Before that, a bit count
    then three biased integers.
    """
    if eng >= ENG_DOUBLE_VECTORS:
        info = b.serialized_int(1 << 7)
        bits = info & 63
        scaled = info >> 6
        if bits:
            sign = 1 << (bits - 1)
            xyz = [((b.bits(bits) ^ sign) - sign) for _ in range(3)]
            if scaled:
                return Vec(xyz[0] / scale, xyz[1] / scale, xyz[2] / scale)
            return Vec(float(xyz[0]), float(xyz[1]), float(xyz[2]))
        if scaled:
            return Vec(b.f64(), b.f64(), b.f64())
        return Vec(b.f32(), b.f32(), b.f32())
    bits = b.serialized_int(max_bits)
    bias = 1 << (bits + 1)
    top = 1 << (bits + 2)
    return Vec(*((b.serialized_int(top) - bias) / scale for _ in range(3)))


def iterate(replay: ReplayFile, buf: bytes) -> Iterator[tuple[float, Actor | None, str, int, str, BitReader]]:
    """Every replicated property as (time, actor, group path, object, name, bits); for exploring a replay."""
    out: list = []
    s = Stream(replay, buf, on_property=lambda t, a, g, o, n, bits: out.append((t, a, g.path, o, n, bits)))
    s.run()
    yield from out
