"""
The replay file: Unreal's local file streamer layout, and the demo header.

A `.replay` written by Unreal's local file network replay streamer is an info
block followed by chunks, each a uint32 type and an int32 size:

    info     magic 0x1CA2E27F, file version, [custom versions], length in ms,
             network version, changelist, friendly name, live flag,
             [timestamp], [compressed flag], [encrypted flag and key]
    chunk 0  header - the FNetworkDemoHeader (magic 0x2CF5A13D): engine and
             game versions, the levels, the header flags
    chunk 1  replay data - start and end time, size, [memory size], then the
             frames (see `stream.py`)
    chunk 2  checkpoint - id, group, metadata, start and end time, size, data
    chunk 3  event - the same layout as a checkpoint; games put their own
             timeline here

The square brackets are fields that only exist from some file version on.
The facts here are from the engine's file format as generic readers
document it (Unreal.Core in FortniteReplayDecompressor, MIT) and were checked
against real Squad v10.3.1 server demos.

Compressed or encrypted replays are refused: their payload is a game's own
compression or key, and neither is used by Squad's server demos.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass, field

from .bits import ByteReader, ReadError

FILE_MAGIC = 0x1CA2E27F
DEMO_MAGIC = 0x2CF5A13D

# The local file streamer's own versions (ELocalFileVersionHistory).
FILE_COMPRESSION = 2
FILE_TIMESTAMP = 3
FILE_CHUNK_TIMES = 4
FILE_ENCRYPTION = 6
FILE_CUSTOM_VERSIONS = 7

CHUNK_HEADER = 0
CHUNK_DATA = 1
CHUNK_CHECKPOINT = 2
CHUNK_EVENT = 3

# The demo header's versions (ENetworkVersionHistory) that change its layout.
NET_MULTIPLE_LEVELS = 6
NET_HEADER_FLAGS = 9
NET_LEVEL_STREAMING_FIXES = 10
NET_FULL_ENGINE_VERSION = 11
NET_HEADER_GUID = 12
NET_PACKAGE_VERSIONS = 17
NET_RECORDING_METADATA = 18
NET_CUSTOM_VERSIONS = 19

# Header flags (EReplayHeaderFlags).
FLAG_CLIENT_RECORDED = 1
FLAG_STREAMING_FIXES = 2
FLAG_DELTA_CHECKPOINTS = 4
FLAG_GAME_SPECIFIC_FRAME_DATA = 8

#: .NET ticks (100 ns since 0001-01-01) at the Unix epoch.
TICKS_AT_UNIX = 621355968000000000


@dataclass
class Chunk:
    kind: int
    offset: int  # where the chunk's own bytes start in the file
    size: int
    start_ms: int = 0
    end_ms: int = 0
    data_offset: int = 0  # where the payload starts
    data_size: int = 0
    id: str = ""
    group: str = ""
    metadata: str = ""


@dataclass
class DemoHeader:
    network_version: int = 0
    network_checksum: int = 0
    engine_network_version: int = 0
    game_network_version: int = 0
    guid: str = ""
    engine_version: tuple[int, int, int] = (0, 0, 0)
    changelist: int = 0
    branch: str = ""
    levels: list[tuple[str, int]] = field(default_factory=list)
    flags: int = 0
    game_specific: list[str] = field(default_factory=list)
    platform: str = ""
    min_record_hz: float | None = None
    max_record_hz: float | None = None

    @property
    def streaming_fixes(self) -> bool:
        return bool(self.flags & FLAG_STREAMING_FIXES)

    @property
    def game_specific_frame_data(self) -> bool:
        return bool(self.flags & FLAG_GAME_SPECIFIC_FRAME_DATA)

    @property
    def delta_checkpoints(self) -> bool:
        return bool(self.flags & FLAG_DELTA_CHECKPOINTS)


@dataclass
class ReplayFile:
    file_version: int
    length_ms: int
    network_version: int
    changelist: int
    friendly_name: str
    live: bool
    recorded_unix: float | None
    compressed: bool
    encrypted: bool
    chunks: list[Chunk]
    header: DemoHeader | None = None

    def data_chunks(self) -> list[Chunk]:
        return [c for c in self.chunks if c.kind == CHUNK_DATA]

    def events(self) -> list[Chunk]:
        return [c for c in self.chunks if c.kind == CHUNK_EVENT]

    def checkpoints(self) -> list[Chunk]:
        return [c for c in self.chunks if c.kind == CHUNK_CHECKPOINT]


def read(buf: bytes) -> ReplayFile:
    """The info block and the chunk table of a replay; the header chunk is parsed too."""
    r = ByteReader(buf)
    if len(buf) < 8 or r.u32() != FILE_MAGIC:
        raise ReadError("not an Unreal local replay (wrong magic)")
    version = r.u32()
    if version >= FILE_CUSTOM_VERSIONS:
        n = r.i32()
        if n < 0 or n > 4096:
            raise ReadError(f"{n} custom versions")
        r.skip(n * 20)  # each a 16-byte GUID and an int32
    length_ms = r.u32()
    network_version = r.u32()
    changelist = r.u32()
    friendly = r.fstring().rstrip()
    live = r.u32() != 0
    recorded = None
    if version >= FILE_TIMESTAMP:
        ticks = r.i64()
        recorded = (ticks - TICKS_AT_UNIX) / 1e7 if ticks > TICKS_AT_UNIX else None
    compressed = r.u32() != 0 if version >= FILE_COMPRESSION else False
    encrypted = False
    if version >= FILE_ENCRYPTION:
        encrypted = r.u32() != 0
        key_len = r.i32()
        if key_len < 0 or key_len > 1024:
            raise ReadError(f"encryption key of {key_len} bytes")
        r.skip(key_len)
    out = ReplayFile(version, length_ms, network_version, changelist, friendly, live, recorded, compressed,
                     encrypted, [])
    while r.left() >= 8:
        kind = r.u32()
        size = r.i32()
        start = r.pos
        if size < 0 or start + size > len(buf):
            raise ReadError(f"chunk {kind} of {size} bytes at {start} runs past the end of the file")
        out.chunks.append(_chunk(buf, kind, start, size, version))
        r.pos = start + size
    for c in out.chunks:
        if c.kind == CHUNK_HEADER:
            out.header = read_header(buf[c.offset : c.offset + c.size])
            break
    return out


def _chunk(buf: bytes, kind: int, start: int, size: int, version: int) -> Chunk:
    c = Chunk(kind, start, size, data_offset=start, data_size=size)
    r = ByteReader(buf, start, start + size)
    if kind == CHUNK_DATA:
        if version >= FILE_CHUNK_TIMES:
            c.start_ms = r.u32()
            c.end_ms = r.u32()
            c.data_size = r.i32()
            if version >= FILE_ENCRYPTION:
                r.i32()  # the size in memory, after decompression
        c.data_offset = r.pos
    elif kind in (CHUNK_CHECKPOINT, CHUNK_EVENT):
        c.id = r.fstring()
        c.group = r.fstring()
        c.metadata = r.fstring()
        c.start_ms = r.u32()
        c.end_ms = r.u32()
        c.data_size = r.i32()
        c.data_offset = r.pos
    if c.data_size < 0 or c.data_offset + c.data_size > start + size:
        raise ReadError(f"chunk {kind} at {start} declares {c.data_size} bytes of data it does not hold")
    return c


def read_header(buf: bytes) -> DemoHeader:
    """The FNetworkDemoHeader in the header chunk."""
    r = ByteReader(buf)
    if r.u32() != DEMO_MAGIC:
        raise ReadError("the header chunk does not start with the demo magic")
    h = DemoHeader(network_version=r.u32())
    v = h.network_version
    if v >= NET_CUSTOM_VERSIONS:
        n = r.i32()
        if n < 0 or n > 4096:
            raise ReadError(f"{n} custom versions in the header")
        r.skip(n * 20)
    h.network_checksum = r.u32()
    h.engine_network_version = r.u32()
    h.game_network_version = r.u32()
    if v >= NET_HEADER_GUID:
        h.guid = r.bytes(16).hex()
    if v >= NET_FULL_ENGINE_VERSION:
        h.engine_version = (r.u16(), r.u16(), r.u16())
        h.changelist = r.u32()
        h.branch = r.fstring()
    else:
        h.changelist = r.u32()
    if v >= NET_PACKAGE_VERSIONS:
        r.skip(12)  # the UE4 and UE5 package versions and the licensee version
    if v >= NET_MULTIPLE_LEVELS:
        n = r.i32()
        if n < 0 or n > 65536:
            raise ReadError(f"{n} levels in the header")
        for _ in range(n):
            name = r.fstring()
            h.levels.append((name, r.u32()))
    else:
        h.levels.append((r.fstring(), 0))
    if v >= NET_HEADER_FLAGS:
        h.flags = r.u32()
    n = r.i32()
    if n < 0 or n > 65536:
        raise ReadError(f"{n} game-specific header entries")
    h.game_specific = [r.fstring() for _ in range(n)]
    if v >= NET_RECORDING_METADATA:
        try:
            h.min_record_hz = r.f32()
            h.max_record_hz = r.f32()
            r.f32()  # frame limit, ms
            r.f32()  # checkpoint limit, ms
            h.platform = r.fstring()
        except ReadError:
            pass  # a trailer this reader does not need
    return h


# ------------------------------------------------------------------ writing
# Only for tests: builds files in the same layout, so the reader can be
# checked on data whose every field is known.


def _fstring(s: str) -> bytes:
    if not s:
        return struct.pack("<i", 0)
    try:
        raw = s.encode("ascii") + b"\x00"
        return struct.pack("<i", len(raw)) + raw
    except UnicodeEncodeError:
        raw = s.encode("utf-16-le") + b"\x00\x00"
        return struct.pack("<i", -(len(raw) // 2)) + raw


def build_header(h: DemoHeader) -> bytes:
    out = struct.pack("<II", DEMO_MAGIC, h.network_version)
    if h.network_version >= NET_CUSTOM_VERSIONS:
        out += struct.pack("<i", 0)
    out += struct.pack("<III", h.network_checksum, h.engine_network_version, h.game_network_version)
    if h.network_version >= NET_HEADER_GUID:
        out += bytes.fromhex(h.guid) if h.guid else bytes(16)
    if h.network_version >= NET_FULL_ENGINE_VERSION:
        out += struct.pack("<HHHI", *h.engine_version, h.changelist) + _fstring(h.branch)
    else:
        out += struct.pack("<I", h.changelist)
    if h.network_version >= NET_PACKAGE_VERSIONS:
        out += bytes(12)
    out += struct.pack("<i", len(h.levels))
    for name, t in h.levels:
        out += _fstring(name) + struct.pack("<I", t)
    if h.network_version >= NET_HEADER_FLAGS:
        out += struct.pack("<I", h.flags)
    out += struct.pack("<i", len(h.game_specific)) + b"".join(_fstring(s) for s in h.game_specific)
    if h.network_version >= NET_RECORDING_METADATA:
        out += struct.pack("<fff f", h.min_record_hz or 0, h.max_record_hz or 0, 0, 0) + _fstring(h.platform)
        out += b"\x00\x00"
    return out


def build(
    header: DemoHeader,
    data: list[tuple[int, int, bytes]],
    events: list[tuple[str, str, str, int, int, bytes]] = (),
    *,
    file_version: int = FILE_CUSTOM_VERSIONS,
    length_ms: int = 0,
    friendly: str = "test",
    recorded_unix: float | None = None,
    compressed: bool = False,
    encrypted: bool = False,
) -> bytes:
    """A replay file: `data` is (start ms, end ms, frames); `events` (id, group, meta, start, end, payload)."""
    out = struct.pack("<II", FILE_MAGIC, file_version)
    if file_version >= FILE_CUSTOM_VERSIONS:
        out += struct.pack("<i", 1) + bytes(16) + struct.pack("<i", 1)
    out += struct.pack("<III", length_ms, header.network_version, header.changelist)
    out += _fstring(friendly) + struct.pack("<I", 0)
    if file_version >= FILE_TIMESTAMP:
        ticks = int(recorded_unix * 1e7) + TICKS_AT_UNIX if recorded_unix is not None else 0
        out += struct.pack("<q", ticks)
    if file_version >= FILE_COMPRESSION:
        out += struct.pack("<I", int(compressed))
    if file_version >= FILE_ENCRYPTION:
        out += struct.pack("<Ii", int(encrypted), 0)

    def chunk(kind: int, body: bytes) -> bytes:
        return struct.pack("<Ii", kind, len(body)) + body

    out += chunk(CHUNK_HEADER, build_header(header))
    for start, end, frames in data:
        body = b""
        if file_version >= FILE_CHUNK_TIMES:
            body += struct.pack("<IIi", start, end, len(frames))
            if file_version >= FILE_ENCRYPTION:
                body += struct.pack("<i", len(frames))
        out += chunk(CHUNK_DATA, body + frames)
    for eid, group, meta, start, end, payload in events:
        body = _fstring(eid) + _fstring(group) + _fstring(meta) + struct.pack("<IIi", start, end, len(payload))
        out += chunk(CHUNK_EVENT, body + payload)
    return out
