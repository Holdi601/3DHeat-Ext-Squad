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
actor or one of its subobjects, a list of (property handle, bit count, bits),
then its remote calls and custom-delta fields, each a (field handle, bit
count, bits) of the class's `_ClassNetCache` export group.

What makes a replay readable without the game's code is that the demo driver
writes the *names* too: the net field export groups map each class path and
property handle to the property's name, and the exported net GUIDs map object
ids to paths. Every property can be found by name; decoding the bits still
needs the property's type, which this module leaves to its caller
(`movement.py` for the engine's own FRepMovement, `squad.py` for the rest).
A remote call's parameters are themselves exported as a group (the
function's path, `/Script/Squad.SQWeapon:MulticastFireProjectile`), and are
read like properties.

With a `Keeper` (`keep.py`) the stream also hands over every item it meets,
whole, so nothing of the demo is lost to what is decoded.

The layout is the engine's, as generic readers document it (Unreal.Core in
FortniteReplayDecompressor, MIT); the version checks are against
EEngineNetworkVersionHistory, and the whole path was checked on real Squad
v10.3.1 server demos (engine network version 36).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Callable, Iterator

from .bits import BitReader, ByteReader, ReadError, concat
from .container import DemoHeader, ReplayFile
from .keep import DECODED, PARTIAL, RAW, Keeper, understood

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

#: EChannelCloseReason, the number a closing bunch carries.
CLOSE_REASONS = ("Destroyed", "Dormancy", "LevelUnloaded", "Relevancy", "TearOff")


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
    scale: Vec | None = None
    velocity: Vec | None = None
    close_reason: str | None = None


@dataclass
class Group:
    path: str
    size: int
    fields: dict[int, str] = field(default_factory=dict)
    leaf: str = ""


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
    rpcs: int = 0
    errors: int = 0
    error_samples: list[str] = field(default_factory=list)

    def error(self, where: str, e: Exception) -> None:
        self.errors += 1
        if len(self.error_samples) < 20:
            self.error_samples.append(f"{where}: {e}")


#: on_property(time, actor or None, group, object guid, property name, bits) -> what is read of it (or None)
PropertySink = Callable[[float, "Actor | None", Group, int, str, BitReader], Any]
#: on_rpc(time, actor, class group, object guid, function name, parameters by name)
RpcSink = Callable[[float, "Actor", Group, int, str, dict], None]


class Stream:
    """
    Reads every data chunk of a replay and reports actors and properties.

    `on_open(actor)`, `on_close(actor)` and `on_property(...)` are called as
    the stream goes; `on_property` only for the property names in `wanted`
    (all of them when `wanted` is None), so the bits nobody asked for are
    skipped, not decoded. `on_rpc` gets every remote call whose parameters
    read, `decode_value(name, bits)` reads a parameter's value. With `keep`
    every item met is also kept, whole (see `keep.py`).
    """

    def __init__(self, replay: ReplayFile, buf: bytes, *, wanted: set[str] | None = None,
                 on_open: Callable[[Actor], None] | None = None,
                 on_close: Callable[[Actor], None] | None = None,
                 on_property: PropertySink | None = None,
                 on_rpc: RpcSink | None = None,
                 decode_value: Callable[[str, BitReader], Any] | None = None,
                 keep: Keeper | None = None):
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
        self.on_rpc = on_rpc
        self.decode_value = decode_value
        self.keep = keep
        self.stats = Stats()
        self.guid_paths: dict[int, str] = {}
        #: guid -> its outer's guid, for exported GUIDs that have one
        self.guid_outers: dict[int, int] = {}
        self.groups: dict[str, Group] = {}
        self.group_by_index: dict[int, Group] = {}
        self._by_leaf: dict[str, Group] = {}
        self._resolved: dict[str, Group | None] = {}
        self._functions: dict[str, list[Group]] | None = None
        self.channels: dict[int, Actor] = {}
        self.actors: dict[int, Actor] = {}
        self._partial: dict[int, tuple[int, int]] = {}  # channel -> (bits, count)
        self._partial_open: dict[int, bool] = {}
        self._partial_head: dict[int, dict] = {}
        self._kinds: dict[str, str] = {}
        self.time = 0.0
        #: (time, value) where the frames' level index, and the packets' level (streaming fixes), changed
        self.level_changes: list[tuple[float, int]] = []
        self.packet_level_changes: list[tuple[float, int]] = []
        #: bunches that named must-be-mapped GUIDs, and channel kinds by name as opening bunches gave them
        self.must_be_mapped = 0
        self.channel_names: dict[str, int] = {}
        self.close_reasons: dict[str, int] = {}
        #: The frame each (group path, handle) was exported in, and what each frame exported: the demo driver
        #: exports a field in the frame it is first sent, which is what names the classes of objects the stream
        #: does not name (see `_resolve`).
        self._frame_no = 0
        self.export_frames: dict[tuple[str, int], int] = {}
        self._exports_in: dict[int, set[tuple[str, int]]] = {}
        #: Bit counts each (group path, handle) was sent with by objects the stream names.
        self.sizes: dict[tuple[str, int], set[int]] = {}
        #: Blocks of objects the stream does not name, read once the whole demo is known.
        self._deferred: list[tuple] = []
        self._keys: dict[tuple, dict[int, list]] = {}
        #: key (actor path, or actor class and subobject name) -> (group, how it was found, blocks)
        self.resolution: dict[tuple, tuple[Group | None, str, int]] = {}
        self.resolution_check: dict[str, int] = {}
        #: subobject guid -> the actor it was sent on
        self.subobjects: dict[int, int] = {}

    # ------------------------------------------------------------- frames

    def run(self) -> Stats:
        k = self.keep
        for c in self.replay.data_chunks():
            r = ByteReader(self.buf, c.data_offset, c.data_offset + c.data_size)
            if k:
                k.meet("chunk.replayData")
            whole = True
            while r.left() > 0:
                start = r.pos
                try:
                    self._frame(r)
                except ReadError as e:
                    # A frame that does not parse leaves the reader nowhere
                    # trustworthy in this chunk; go on with the next one.
                    self.stats.error(f"frame at byte {r.pos}", e)
                    if k:
                        k.packet("frame", RAW, self.time, "frame.rest", "", None, start,
                                 {"error": str(e), "chunkStartMs": c.start_ms}, data=self.buf[start : r.end])
                    whole = False
                    break
            if k:
                k.put("chunk.replayData", DECODED if whole else PARTIAL)
        self._unfinished_partials()
        self._resolve()
        self._read_deferred()
        return self.stats

    def _unfinished_partials(self) -> None:
        """Partial bunches whose final part never came: kept whole."""
        for ch, (value, count) in list(self._partial.items()):
            if self.keep:
                self.keep.meet("bunch")
                self.keep.packet("bunch", RAW, self.time, "bunch.unfinished", "", ch, None,
                                 self._partial_head.get(ch), value=value, count=count)
        self._partial.clear()

    def _frame(self, r: ByteReader) -> None:
        k = self.keep
        if k:
            k.meet("frame")
        self.stats.frames += 1
        self._frame_no += 1
        level = r.i32() if self.h.network_version >= 6 else None  # the current level's index
        self.time = r.f32()
        if level is not None and (not self.level_changes or self.level_changes[-1][1] != level):
            self.level_changes.append((self.time, level))
        if self.h.network_version >= 10:
            self._field_exports(r)
            self._guid_exports(r)
        if self.h.streaming_fixes:
            self._streaming_levels(r)
            r.u64()  # the offset of the external data, for seeking
            self._external(r)
        else:
            self._external(r)
            # In the layout without streaming fixes a (normally empty) list of
            # streaming level names follows the external data.
            self._streaming_levels(r)
        if self.h.game_specific_frame_data:
            n = r.u64()
            at = r.pos
            data = r.bytes(n)
            if k:
                k.meet("frame.gameData")
                k.packet("frame.gameData", RAW, self.time, "frame.gameData", "", None, at, None, data=data)
        while True:
            if self.h.streaming_fixes:
                pl = r.packed()  # the level the packet was seen in
                if not self.packet_level_changes or self.packet_level_changes[-1][1] != pl:
                    self.packet_level_changes.append((self.time, pl))
            size = r.i32()
            if size <= 0:
                if k:
                    k.decoded("frame")
                return  # 0 ends the frame's packets (a negative size marks the end of a checkpoint)
            at = r.pos
            data = r.bytes(size)
            self.stats.packets += 1
            if k:
                k.meet("packet")
            done = self.stats.bunches
            try:
                self._packet(data)
                if k:
                    k.decoded("packet")
            except ReadError as e:
                self.stats.error(f"packet at {self.time:.2f}s", e)
                if k:
                    read = self.stats.bunches - done
                    k.packet("packet", PARTIAL if read else RAW, self.time, "packet", "", None, at,
                             {"error": str(e), "bunchesRead": read}, data=data)

    def _streaming_levels(self, r: ByteReader) -> None:
        n = r.packed()
        if not n:
            return
        at = r.pos
        names = [r.fstring() for _ in range(n)]
        if self.keep:
            self.keep.meet("frame.streamingLevels")
            self.keep.packet("frame.streamingLevels", PARTIAL, self.time, "frame.streamingLevels", "", None, at,
                             {"levels": names}, data=self.buf[at : r.pos])

    def _field_exports(self, r: ByteReader) -> None:
        k = self.keep
        for _ in range(r.packed()):
            at = r.pos
            index = r.packed()
            new_path = None
            if r.packed():
                path = r.fstring()
                size = r.packed()
                new_path = path
                g = self.groups.get(path)
                if g is None:
                    g = self.groups[path] = Group(path, size, leaf=_leaf(path))
                    self._by_leaf.setdefault(g.leaf, g)
                    self._resolved.clear()
                    self._functions = None
                self.group_by_index[index] = g
            g = self.group_by_index.get(index)
            handle = name = checksum = None
            if r.u8():
                handle = r.packed()
                checksum = r.u32()  # the property's compatibility checksum
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
                    if (g.path, handle) not in self.export_frames:
                        self.export_frames[(g.path, handle)] = self._frame_no
                        self._exports_in.setdefault(self._frame_no, set()).add((g.path, handle))
            if k:
                k.meet("export.field")
                k.entity_bytes("export.field", PARTIAL, self.time, g.path if g else f"#group{index}",
                               name or "", None, "export.field",
                               {"index": index, "group": g.path if g else None, "newGroup": new_path is not None,
                                "size": g.size if g else None, "handle": handle, "name": name,
                                "checksum": checksum}, self.buf[at : r.pos], group=g.path if g else "",
                               handle=handle)

    def _guid_exports(self, r: ByteReader) -> None:
        for _ in range(r.packed()):
            size = r.i32()
            data = r.bytes(size)
            if self.keep:
                self.keep.meet("export.guid")
            chain: list = []
            try:
                guid = self._net_guid(BitReader.from_bytes(data), exporting=True, chain=chain)
            except ReadError as e:
                self.stats.error("exported net GUID", e)
                if self.keep:
                    self.keep.entity_bytes("export.guid", RAW, self.time, "export.guid", "", None, "export.guid",
                                           {"error": str(e)}, data)
                continue
            if self.keep:
                self.keep.entity_bytes("export.guid", PARTIAL, self.time, "export.guid",
                                       self.guid_paths.get(guid, ""), guid, "export.guid", {"chain": chain}, data)

    def _external(self, r: ByteReader) -> None:
        # Properties some actors hand the demo driver outside their bunches.
        while True:
            bits = r.packed()
            if bits == 0:
                return
            guid = r.packed()  # the actor's net GUID
            data = r.bytes((bits + 7) // 8)
            self.stats.external += 1
            if self.keep:
                self.keep.meet("external")
                a = self.actors.get(guid)
                self.keep.entity("external", RAW, self.time, "external", self._kind(a), guid, "external", guid,
                                 a.channel if a else None, None, "", None, int.from_bytes(data, "little"), bits)

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
        k = self.keep
        if eng < ENG_NO_EXTRA_BUNCH_BIT:
            p.bit()
        control = p.bit()
        opening = control and p.bit()
        closing = control and p.bit()
        reason = None
        if closing:
            if eng < ENG_CHANNEL_CLOSE_REASON:
                reason = 0 if p.bit() else None  # dormant or not
            else:
                reason = p.serialized_int(15)
        p.bit()  # replication paused
        reliable = p.bit()
        ch = p.packed() if eng >= ENG_CHANNEL_INDEX_PACKED else p.serialized_int(1 << 32)
        has_exports = p.bit()
        must_be_mapped = p.bit()
        partial = p.bit()
        partial_initial = partial and p.bit()
        if partial and eng >= ENG_PARTIAL_CUSTOM_EXPORTS:
            p.bit()  # custom exports final
        partial_final = partial and p.bit()
        channel_name = None
        if eng >= ENG_CHANNEL_NAMES and (reliable or opening):
            channel_name = p.fname()  # the channel's kind: Actor, Control, Voice
        n = p.serialized_int(MAX_BUNCH_BITS)
        body = p.window(n)
        self.stats.bunches += 1
        if k:
            k.meet("bunch")
        head = {"channel": ch, "opening": opening, "closing": closing, "reliable": reliable,
                "partial": partial, "initial": partial_initial, "final": partial_final} if k else None
        if closing and reason is not None:
            name = CLOSE_REASONS[reason] if reason < len(CLOSE_REASONS) else f"#{reason}"
            self.close_reasons[name] = self.close_reasons.get(name, 0) + 1
            if head is not None:
                head["closeReason"] = name
        if channel_name is not None and opening:
            self.channel_names[channel_name] = self.channel_names.get(channel_name, 0) + 1
        if has_exports:
            try:
                if body.bit():
                    raise ReadError("rep layout exports inside a bunch")
                count = body.i32()
                if count < 0 or count > 2048:
                    raise ReadError(f"{count} GUIDs exported in a bunch")
                for _ in range(count):
                    at = body.pos
                    chain: list = []
                    guid = self._net_guid(body, exporting=True, chain=chain)
                    if k:
                        k.meet("export.guid")
                        k.entity("export.guid", PARTIAL, self.time, "export.guid", self.guid_paths.get(guid, ""),
                                 guid, "export.guid", guid, ch, None, "", {"chain": chain, "inBunch": True},
                                 body.value >> at, body.pos - at)
            except ReadError:
                if k:
                    k.put("bunch", RAW)  # kept whole in the packet's row
                raise
        if partial:
            if partial_initial:
                if ch in self._partial:
                    # A new start before the last one ended: the last one is kept as it was.
                    value, count = self._partial.pop(ch)
                    if k:
                        k.meet("bunch")
                        k.packet("bunch", RAW, self.time, "bunch.unfinished", "", ch, None,
                                 self._partial_head.get(ch), value=value, count=count)
                self._partial[ch] = body.rest()
                self._partial_open[ch] = opening
                self._partial_head[ch] = {**(head or {}), "mustBeMapped": must_be_mapped, "channelName": channel_name}
                if not partial_final:
                    if k:
                        k.decoded("bunch")  # its bits go on in the joined bunch
                    return
            elif ch in self._partial:
                rest = body.rest()
                if not has_exports:
                    self._partial[ch] = concat(self._partial[ch], rest)
                elif rest[1] and k:
                    # Bits after a part's exports, which the joined bunch does not take: kept.
                    k.meet("bunch.leftover")
                    k.packet("bunch.leftover", RAW, self.time, "bunch.leftover", "", ch, None, head,
                             value=rest[0], count=rest[1])
                if not partial_final:
                    if k:
                        k.decoded("bunch")
                    return
            else:
                # The rest of a bunch whose start was not recorded.
                if k:
                    value, count = body.rest()
                    k.packet("bunch", RAW, self.time, "bunch.orphan", "", ch, None, head, value=value, count=count)
                return
            value, count = self._partial.pop(ch)
            opening = self._partial_open.pop(ch, opening)
            first = self._partial_head.pop(ch, {})
            must_be_mapped = first.get("mustBeMapped", must_be_mapped)
            channel_name = first.get("channelName", channel_name)
            body = BitReader(value, count)
        whole = body.rest() if k else None
        try:
            if must_be_mapped:
                self.must_be_mapped += 1
                # The GUIDs the receiver must know before it takes the bunch: a count, then the GUIDs.
                for _ in range(body.u16()):
                    body.packed()
            routed = self._channel_bunch(ch, opening, body, channel_name)
            if k:
                if routed:
                    k.decoded("bunch")
                else:
                    k.packet("bunch", RAW, self.time, "bunch.unopened", "", ch, None, head,
                             value=whole[0], count=whole[1])
        except ReadError as e:
            self.stats.error(f"channel {ch} at {self.time:.2f}s", e)
            if k:
                # What was read of it is kept as read; the bunch itself is kept whole.
                k.packet("bunch", PARTIAL, self.time, "bunch.error", self._kind(self.channels.get(ch)), ch, None,
                         {**(head or {}), "error": str(e)}, value=whole[0], count=whole[1])
        if closing:
            actor = self.channels.pop(ch, None)
            if actor is not None:
                actor.closed = self.time
                actor.close_reason = head["closeReason"] if head else (
                    CLOSE_REASONS[reason] if reason is not None and reason < len(CLOSE_REASONS) else None)
                if self.on_close:
                    self.on_close(actor)
            if k:
                k.meet("close")
                k.entity("close", PARTIAL, self.time, "close", self._kind(actor), actor.guid if actor else None,
                         "close", actor.guid if actor else None, ch, None, "",
                         {"reason": head.get("closeReason"), "known": actor is not None})

    # ------------------------------------------------------------- objects

    def _net_guid(self, r: BitReader, exporting: bool, depth: int = 0, chain: list | None = None) -> int:
        """A net GUID; when it is exported (or the default), its outer and path follow."""
        if depth > 16:
            raise ReadError("net GUID outers nested too deep")
        guid = r.packed()
        if guid == 0:
            return 0
        if guid == 1 or exporting:
            flags = r.u8()
            if flags & 1:  # has path
                outer = self._net_guid(r, True, depth + 1, chain)
                path = r.fstring()
                checksum = r.u32() if flags & 4 else None  # has network checksum
                if exporting:
                    self.guid_paths[guid] = path
                    if outer:
                        self.guid_outers[guid] = outer
                if chain is not None:
                    chain.append({"guid": guid, "flags": flags, "outer": outer, "path": path, "checksum": checksum})
            elif chain is not None:
                chain.append({"guid": guid, "flags": flags})
        return guid

    def _kind(self, actor: Actor | None) -> str:
        """An actor's class, as its archetype's path ends."""
        if actor is None:
            return ""
        k = self._kinds.get(actor.path)
        if k is None:
            k = self._kinds[actor.path] = _leaf(actor.path)
        return k

    def _channel_bunch(self, ch: int, opening: bool, b: BitReader, channel_name: str | None = None) -> bool:
        """The bunch's content; False when it belongs to no actor this recording opened."""
        actor = self.channels.get(ch)
        if actor is None:
            if not opening:
                return b.at_end()  # a channel opened before the recording, or only being closed
            if b.at_end():
                if self.keep:
                    self.keep.meet("open")
                    self.keep.entity("open", PARTIAL, self.time, "open", "", None, "open", None, ch, None, "",
                                     {"channelName": channel_name, "empty": True})
                return True
            actor = self._spawn(ch, b, channel_name)
        while not b.at_end():
            self._content_block(actor, b, ch)
        return True

    def _spawn(self, ch: int, b: BitReader, channel_name: str | None = None) -> Actor:
        if self.keep:
            self.keep.meet("open")
        try:
            return self._spawn_actor(ch, b, channel_name)
        except ReadError:
            if self.keep:
                self.keep.put("open", RAW)  # kept whole in the bunch's row
            raise

    def _spawn_actor(self, ch: int, b: BitReader, channel_name: str | None) -> Actor:
        start = b.pos
        a = Actor(guid=self._net_guid(b, False), channel=ch, opened=self.time)
        if a.guid and not a.guid & 1 and not b.at_end():  # dynamic: spawned, so its spawn info follows
            a.archetype = self._net_guid(b, False)
            if self.eng >= ENG_LEVEL_IN_SPAWN:
                a.level = self._net_guid(b, False)
            a.location = self._optional_vector(b, Vec())
            if b.bit():
                a.rotation = tuple(b.u16() * 360.0 / 65536.0 if b.bit() else 0.0 for _ in range(3))
            a.scale = self._optional_vector(b, Vec(1, 1, 1))
            a.velocity = self._optional_vector(b, Vec())
            a.path = self.guid_paths.get(a.archetype, "")
        else:
            a.path = self.guid_paths.get(a.guid, "")
        old = self.actors.get(a.guid)
        reopened = old is not None and a.archetype is None
        if reopened:
            # A channel opened again for an actor already known (after it went dormant): the same actor, on a new
            # channel; the open carries no spawn data.
            old.channel, old.closed, old.close_reason = ch, None, None
            a = old
        self.channels[ch] = a
        self.actors[a.guid] = a
        self.stats.actor_opens += 1
        if self.keep:
            self.keep.entity("open", PARTIAL, self.time, "open", self._kind(a), a.guid, "open", a.guid, ch, None,
                             a.path, {"channelName": channel_name, "reopened": reopened,
                                      "archetype": None if reopened else a.archetype, "path": a.path,
                                      "level": None if reopened else a.level,
                                      "location": None if reopened else _xyz(a.location),
                                      "rotation": None if reopened else a.rotation,
                                      "scale": None if reopened else _xyz(a.scale),
                                      "velocity": None if reopened else _xyz(a.velocity)},
                             b.value >> start, b.pos - start)
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

    def _content_block(self, actor: Actor, b: BitReader, ch: int | None = None) -> None:
        self.stats.content_blocks += 1
        k = self.keep
        start = b.pos
        has_rep_layout = b.bit()
        stable = cls = outer = None
        is_actor = b.bit()
        if is_actor:  # the actor itself
            obj = actor.guid
            path = actor.path
        else:
            obj = self._net_guid(b, False)
            self.subobjects[obj] = actor.guid
            stable = b.bit()
            if stable:  # stably named: its path is known from the exports
                path = self.guid_paths.get(obj, "")
            else:
                if self.eng >= ENG_SUBOBJECT_DESTROY_FLAG and b.bit():
                    flags = b.u8()  # destroy flags
                    if k:
                        k.meet("subobject.destroy")
                        k.entity("subobject.destroy", PARTIAL, self.time, "subobject.destroy", self._kind(actor),
                                 actor.guid, "subobject.destroy", obj, ch, None, "", {"flags": flags},
                                 b.value >> start, b.pos - start)
                    return
                cls = self._net_guid(b, False)
                if cls == 0:
                    if k:  # the subobject was deleted
                        k.meet("subobject.deleted")
                        k.entity("subobject.deleted", PARTIAL, self.time, "subobject.deleted", self._kind(actor),
                                 actor.guid, "subobject.deleted", obj, ch, None, "", {},
                                 b.value >> start, b.pos - start)
                    return
                if self.eng >= ENG_SUBOBJECT_OUTER and not b.bit():
                    outer = self._net_guid(b, False)  # its outer, when it is not the actor
                path = self.guid_paths.get(cls, "")
        n = b.packed()
        payload = b.window(n)
        g = self.group_for(path)
        if n == 0:
            if k:  # a block with nothing in it but its header: a subobject made, or an empty update
                k.meet("block.empty")
                k.entity("block.empty", PARTIAL, self.time, f"{g.leaf if g else _leaf(path)}", self._kind(actor),
                         actor.guid, "block.empty", obj, ch, None, g.path if g else path,
                         {"repLayout": has_rep_layout, "stable": stable, "class": cls, "outer": outer},
                         b.value >> start, b.pos - start)
            return
        if g is None:
            # An object the exports do not name (a level's actor by its instance name, a component by its own):
            # its class is found once the whole demo is read, from what it sent and when (`_resolve`).
            key = (path,) if is_actor else (self._kind(actor), path)
            seen = self._keys.setdefault(key, {})
            if has_rep_layout:
                self._scan_handles(payload, seen)
            head = {"repLayout": has_rep_layout, "stable": stable, "class": cls, "outer": outer,
                    "classPath": self.guid_paths.get(cls, "") if cls else None,
                    "objectPath": self.guid_paths.get(obj, "")}
            self._deferred.append((self.time, actor, obj, key, path, has_rep_layout, payload.value, payload.pos, n,
                                   ch, head))
            return
        if has_rep_layout:
            self._properties(actor, g, obj, payload, ch, direct=True)
        if not payload.at_end():
            self._fields(actor, g, obj, payload, ch)

    def _scan_handles(self, payload: BitReader, seen: dict[int, list]) -> None:
        """The handles a block sends and their bit counts, with the frame each handle was first sent in."""
        b = BitReader(payload.value, payload.end, payload.pos)
        try:
            b.bit()
            while not b.at_end():
                handle = b.packed()
                if handle == 0:
                    return
                n = b.packed()
                b.skip(n)
                e = seen.get(handle - 1)
                if e is None:
                    seen[handle - 1] = [self._frame_no, {n}]
                else:
                    e[1].add(n)
        except ReadError:
            return

    def _resolve(self) -> None:
        """
        The class of every object the stream does not name, from the export
        tables: the demo driver exports a class's field in the frame it is
        first sent (true of every first send of a named object in the demos
        checked), so the class is

        1. the one group that exported, in the frame where this object first
           sent each of its handles, exactly those handles ("export frame");
        2. else, among the groups that had all its handles exported by then,
           any - when they all give its handles the same names ("names agree");
        3. else the class of an object of the same name, numbers left out,
           already found ("same name"), or the one group whose name holds the
           object's ("name").

        What none of these settles stays unread, its blocks kept whole.
        """
        groups = [g for g in self.groups.values() if ":" not in g.path and not g.path.endswith("_ClassNetCache")]
        by_name: dict[str, Group] = {}
        rest = []
        counts: dict[tuple, int] = {}
        for item in self._deferred:
            counts[item[3]] = counts.get(item[3], 0) + 1
        candidates: dict[tuple, list[Group]] = {}
        for key, seen in self._keys.items():
            hs = sorted(seen)
            if not hs:
                candidates[key] = []
                rest.append(key)
                continue
            c0 = [g for g in groups if hs[-1] < g.size and all(
                h in g.fields and self.export_frames.get((g.path, h), 1 << 60) <= seen[h][0] for h in hs)]
            candidates[key] = c0
            at = None
            for h in hs:
                here = {p for p, hh in self._exports_in.get(seen[h][0], ()) if hh == h}
                at = here if at is None else at & here
            at = [g for g in c0 if g.path in (at or ())]
            if len(at) == 1:
                self.resolution[key] = (at[0], "export frame", counts.get(key, 0))
                by_name.setdefault(_stem(key[-1]), at[0])
            else:
                rest.append(key)
        # What each class's fields were sent with, by named objects and by those the export frame settled.
        profile: dict[tuple[str, int], set[int]] = {k: set(v) for k, v in self.sizes.items()}
        for key, (g, how, _n) in self.resolution.items():
            for h, (_f, sizes) in self._keys[key].items():
                profile.setdefault((g.path, h), set()).update(sizes)

        def fits(g: Group, seen: dict[int, list]) -> bool:
            """Whether an object's handles came with the bit counts the class's fixed-size fields have."""
            for h, (_f, sizes) in seen.items():
                known = profile.get((g.path, h))
                if known and len(known) == 1 and max(known) <= 64 and sizes != known:
                    return False
            return True

        for key in rest:
            seen = self._keys[key]
            c0 = [g for g in candidates[key] if fits(g, seen)] or candidates[key]
            hs = sorted(seen)
            stem = _stem(key[-1])
            named = by_name.get(stem)
            if hs and c0 and len({tuple(g.fields[h] for h in hs) for g in c0}) == 1:
                g = named if named in c0 else _closest(stem, c0)
                self.resolution[key] = (g, "names agree", counts.get(key, 0))
                continue
            pool = c0 if hs else groups
            if named is not None and named in pool:
                self.resolution[key] = (named, "same name", counts.get(key, 0))
                continue
            close = [g for g in pool if _norm(stem) and (_norm(stem) in _norm(g.leaf) or _norm(g.leaf) in _norm(stem))]
            if len(close) == 1:
                self.resolution[key] = (close[0], "name", counts.get(key, 0))
            elif len(c0) == 1:
                self.resolution[key] = (c0[0], "only fit", counts.get(key, 0))
            else:
                self.resolution[key] = (None, "unresolved", counts.get(key, 0))
        # The check: how many of the handles of objects named here came with the bit counts the class's other
        # objects send them with, where those are one fixed size.
        same = other = 0
        for key, (g, how, _n) in self.resolution.items():
            if g is None or how == "export frame":
                continue
            for h, (_f, sizes) in self._keys[key].items():
                known = profile.get((g.path, h))
                if known and len(known) == 1 and max(known) <= 64:
                    if sizes == known:
                        same += 1
                    else:
                        other += 1
        self.resolution_check = {"handlesWithTheClassSizes": same, "handlesWithOtherSizes": other}

    def _read_deferred(self) -> None:
        """The blocks of objects `_resolve` named, read now, at their own time; the rest kept whole."""
        k = self.keep
        for t, actor, obj, key, path, has_rep_layout, value, pos, n, ch, head in self._deferred:
            self.time = t
            g = self.resolution.get(key, (None,))[0]
            payload = BitReader(value, pos + n, pos)
            if g is not None:
                try:
                    if has_rep_layout:
                        self._properties(actor, g, obj, payload, ch)
                    if not payload.at_end():
                        self._fields(actor, g, obj, payload, ch)
                    continue
                except ReadError as e:
                    head = {**head, "error": str(e), "resolvedAs": g.path}
            self.stats.unresolved_blocks += 1
            if k:
                kind = f"block:{_leaf(path) or '?'}"
                k.meet(kind)
                k.entity(kind, RAW, t, _leaf(path) or "?", self._kind(actor), actor.guid, "block", obj, ch, None,
                         path, head, value >> pos, n)
        self._deferred = []

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

    def _properties(self, actor: Actor, g: Group, obj: int, b: BitReader, ch: int | None = None,
                    direct: bool = False) -> None:
        k = self.keep
        kind = f"property:{g.leaf}"
        b.bit()  # the checksum flag of the backwards-compatible layout
        while not b.at_end():
            handle = b.packed()
            if handle == 0:
                return
            handle -= 1
            n = b.packed()
            bits = b.window(n)
            if k:
                k.meet(kind)
            if direct:
                sizes = self.sizes.get((g.path, handle))
                if sizes is None:
                    self.sizes[(g.path, handle)] = {n}
                elif len(sizes) < 8:
                    sizes.add(n)
            name = g.fields.get(handle)
            if name is None:
                if k:
                    k.entity(kind, RAW, self.time, f"{g.leaf}.#{handle}", self._kind(actor), actor.guid, "property",
                             obj, ch, handle, g.path, None, bits.value >> bits.pos, n)
                continue
            self.stats.properties += 1
            value = None
            if self.on_property and (self.wanted is None or name in self.wanted):
                value = self.on_property(self.time, actor, g, obj, name, bits)
            if k:
                k.entity(kind, PARTIAL if understood(value) else RAW, self.time, f"{g.leaf}.{name}",
                         self._kind(actor), actor.guid, "property", obj, ch, handle, g.path, value,
                         bits.value >> bits.pos, n)

    def _fields(self, actor: Actor, g: Group, obj: int, b: BitReader, ch: int | None) -> None:
        """
        What follows the properties: remote calls and custom-delta fields,
        each a handle into the class's `_ClassNetCache` group, a bit count and
        the bits. A call's parameters are read by the function's own group.
        """
        k = self.keep
        kind = f"rpc:{g.leaf}"
        cache = self.groups.get(g.path + "_ClassNetCache")
        while not b.at_end():
            at = b.pos
            if k:
                k.meet(kind)
            try:
                if cache is None:
                    raise ReadError(f"no _ClassNetCache group for {g.path}")
                handle = b.serialized_int(max(cache.size, 2))
                n = b.packed()
                bits = b.window(n)
            except ReadError as e:
                if k:
                    k.entity(kind, RAW, self.time, f"{g.leaf}.?", self._kind(actor), actor.guid, "fields", obj, ch,
                             None, g.path, {"error": str(e)}, b.value >> at, b.end - at)
                b.pos = b.end
                return
            name = cache.fields.get(handle)
            params = self._rpc_params(name, bits) if name else None
            self.stats.rpcs += 1
            if params is not None and self.on_rpc:
                self.on_rpc(self.time, actor, g, obj, name, params)
            if k:
                k.entity(kind, PARTIAL if params is not None else RAW, self.time, f"{g.leaf}.{name or f'#{handle}'}",
                         self._kind(actor), actor.guid, "rpc", obj, ch, handle, cache.path, params,
                         bits.value >> bits.pos, n)

    def _rpc_params(self, name: str, b: BitReader) -> dict | None:
        """
        A remote call's parameters by name, read by its function's group
        (`<class>:<function>`) like properties; {} for a call that has none;
        None where they do not read (a custom-delta field, a function the
        demo exported no group for).
        """
        if self._functions is None:
            self._functions = {}
            for path, grp in self.groups.items():
                if ":" in path:
                    self._functions.setdefault(path.rsplit(":", 1)[1], []).append(grp)
        candidates = self._functions.get(name, [])
        if not candidates:
            return {} if b.at_end() else None
        for fg in candidates:
            r = BitReader(b.value, b.end, b.pos)
            out: dict[str, Any] = {}
            try:
                if r.at_end():
                    return out
                r.bit()  # the checksum flag, as for properties
                while not r.at_end():
                    handle = r.packed()
                    if handle == 0:
                        break
                    n = r.packed()
                    w = r.window(n)
                    pname = fg.fields.get(handle - 1, f"#{handle - 1}")
                    out[pname] = self.decode_value(pname, w) if self.decode_value else _hex(w)
                if r.at_end():
                    return out
            except ReadError:
                continue
        return None


def _stem(name: str) -> str:
    """An object's name without its instance number: `BP_I_Sandbag_10` -> `BP_I_Sandbag`, `wheel_L1` stays."""
    return re.sub(r"(_C)?_\d+$", "", _leaf(name)) or name


def _norm(name: str) -> str:
    """A class or object name reduced for comparing: no `SQ`/`BP_` prefix, `_C` or `Component` suffix, case."""
    n = re.sub(r"_C$", "", name)
    n = re.sub(r"^(SQ|BP_)", "", n)
    n = re.sub(r"(Component|Comp)$", "", n)
    return re.sub(r"[^a-z0-9]", "", n.lower())


def _closest(stem: str, groups: list[Group]) -> Group:
    """The group whose name shares the most four-letter pieces with `stem` (first of the best)."""
    a = _norm(stem)
    pieces = {a[i : i + 4] for i in range(max(1, len(a) - 3))}

    def score(g: Group) -> int:
        b = _norm(g.leaf)
        return len(pieces & {b[i : i + 4] for i in range(max(1, len(b) - 3))})

    return max(groups, key=score)


def _hex(b: BitReader) -> dict:
    value, count = b.rest()
    return {"bits": count, "hex": value.to_bytes((count + 7) // 8, "little").hex()}


def _xyz(v: Vec | None) -> list[float] | None:
    return [v.x, v.y, v.z] if v is not None else None


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
