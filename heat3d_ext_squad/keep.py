"""
Everything the demo holds that the table and the match document do not hold
whole, kept whole beside them - the rule all 3DHeat converters follow
(https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md).

Two sidecars, next to the table:

- `<match>.entities.parquet`: every actor channel opened and closed (with its
  spawn data and close reason), every replicated property (its handle, its
  bits and what is read of it), every remote call and custom-delta field,
  every content block whose class the stream does not name, every subobject
  deleted, every external data block, and the context a later decoder needs
  to read them alone: every net field export (class path, handle, property
  name, checksum) and every exported net GUID (its path, outer and flags),
  in stream order.
- `<match>.packets.parquet`: everything below that: the container's info
  block, header, checkpoint and event chunks, the game-specific frame data,
  streaming level lists, and every packet, bunch or frame the stream could
  not take apart, whole.

The entities sidecar's rows are grouped by kind, type and entity, each group
in time order; the packets sidecar's are in time order.

Each item is counted where the stream meets it (`meet`) and where it is put
(`decoded`, or a row with a status): what was met and put nowhere shows as
`lost` in `selfCheck.completeness`, under its type.
"""

from __future__ import annotations

import json
import math
from typing import Any

#: Where the rule is written.
RULE = "https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md"

DECODED, PARTIAL, RAW = 0, 1, 2

ENTITY_COLUMNS = ("time", "type", "name", "entity", "kind", "object", "channel", "handle", "group", "decoded", "bits",
                  "payload")
PACKET_COLUMNS = ("time", "type", "name", "channel", "offset", "decoded", "bits", "payload")


def jsonable(v: Any) -> Any:
    """A value JSON can hold: non-finite floats become null, bytes hex, tuples lists."""
    if isinstance(v, float):
        return v if math.isfinite(v) else None
    if isinstance(v, (str, int, bool)) or v is None:
        return v
    if isinstance(v, dict):
        return {str(k): jsonable(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [jsonable(x) for x in v]
    if isinstance(v, (bytes, bytearray)):
        return bytes(v).hex()
    return str(v)


def understood(v: Any) -> bool:
    """Whether a decoded value says anything beyond the bits themselves (a bare {bits, hex} does not)."""
    if v is None:
        return False
    if isinstance(v, dict) and v and set(v) <= {"bits", "hex"}:
        return False
    return True


def to_bytes(value: int, count: int) -> bytes:
    """Bits held as an integer (lowest first), as the bytes they were read from."""
    return (value & ((1 << count) - 1)).to_bytes((count + 7) // 8, "little") if count > 0 else b""


class Keeper:
    """The rows of both sidecars and the counts behind `selfCheck.completeness`."""

    def __init__(self) -> None:
        #: type -> [seen, decoded, partial, raw]
        self.types: dict[str, list[int]] = {}
        self.entities: dict[str, list] = {c: [] for c in ENTITY_COLUMNS}
        self.packets: dict[str, list] = {c: [] for c in PACKET_COLUMNS}

    # ------------------------------------------------------------- counting

    def _t(self, kind: str) -> list[int]:
        c = self.types.get(kind)
        if c is None:
            c = self.types[kind] = [0, 0, 0, 0]
        return c

    def meet(self, kind: str, n: int = 1) -> None:
        """`n` items of this type were met in the source."""
        self._t(kind)[0] += n

    def decoded(self, kind: str, n: int = 1) -> None:
        """`n` items read whole into the table or the match document."""
        self._t(kind)[1] += n

    def put(self, kind: str, status: int, n: int = 1) -> None:
        self._t(kind)[1 + status] += n

    # ------------------------------------------------------------- rows

    def entity(self, kind: str, status: int, t: float, typ: str, name: str, entity: int | None, row_kind: str,
               obj: int | None, channel: int | None, handle: int | None, group: str, decoded: Any,
               value: int = 0, count: int = 0) -> None:
        """A row of the entities sidecar; `value`/`count` are the item's bits (lowest first) and how many."""
        self._t(kind)[1 + status] += 1
        e = self.entities
        e["time"].append(t)
        e["type"].append(typ)
        e["name"].append(name)
        e["entity"].append(entity)
        e["kind"].append(row_kind)
        e["object"].append(obj)
        e["channel"].append(channel)
        e["handle"].append(handle)
        e["group"].append(group)
        e["decoded"].append("" if decoded is None else json.dumps(jsonable(decoded), separators=(",", ":")))
        e["bits"].append(count)
        e["payload"].append(to_bytes(value, count))

    def entity_bytes(self, kind: str, status: int, t: float, typ: str, name: str, entity: int | None, row_kind: str,
                     decoded: Any, data: bytes, group: str = "", handle: int | None = None) -> None:
        """A row of the entities sidecar whose item is whole bytes (the frame's export tables, external data)."""
        self.entity(kind, status, t, typ, name, entity, row_kind, entity, None, handle, group, decoded,
                    int.from_bytes(data, "little"), len(data) * 8)

    def packet(self, kind: str, status: int, t: float | None, typ: str, name: str, channel: int | None,
               offset: int | None, decoded: Any, data: bytes | None = None, value: int = 0, count: int = 0) -> None:
        """A row of the packets sidecar: whole bytes (`data`), or bits (`value`, `count`) where not byte aligned."""
        self._t(kind)[1 + status] += 1
        p = self.packets
        p["time"].append(t)
        p["type"].append(typ)
        p["name"].append(name)
        p["channel"].append(channel)
        p["offset"].append(offset)
        p["decoded"].append("" if decoded is None else json.dumps(jsonable(decoded), separators=(",", ":")))
        if data is not None:
            p["bits"].append(len(data) * 8)
            p["payload"].append(bytes(data))
        else:
            p["bits"].append(count)
            p["payload"].append(to_bytes(value, count))

    # ------------------------------------------------------------- the self-check

    def completeness(self, sidecars: list[str]) -> dict[str, Any]:
        types = {}
        lost_total = 0
        for kind in sorted(self.types):
            seen, dec, part, raw = self.types[kind]
            lost = seen - dec - part - raw
            lost_total += lost
            types[kind] = {"seen": seen, "decoded": dec, "partial": part, "raw": raw, "lost": lost}
        return {"rule": RULE, "sidecars": sidecars, "types": types, "lost": lost_total}

    # ------------------------------------------------------------- writing

    def tables(self):
        """The two sidecars as Arrow tables (None where a sidecar has no rows)."""
        import pyarrow as pa

        def dict_str(v):
            return pa.array(v, pa.string()).dictionary_encode()

        e = self.entities
        ent = None
        if e["time"]:
            ent = pa.table({
                "time": pa.array(e["time"], pa.float64()),
                "type": dict_str(e["type"]),
                "name": dict_str(e["name"]),
                "entity": pa.array(e["entity"], pa.int64()),
                "kind": dict_str(e["kind"]),
                "object": pa.array(e["object"], pa.int64()),
                "channel": pa.array(e["channel"], pa.int32()),
                "handle": pa.array(e["handle"], pa.int32()),
                "group": dict_str(e["group"]),
                "decoded": pa.array(e["decoded"], pa.string()),
                "bits": pa.array(e["bits"], pa.int32()),
                "payload": pa.array(e["payload"], pa.binary()),
            })
        p = self.packets
        pkt = None
        if p["type"]:
            pkt = pa.table({
                "time": pa.array(p["time"], pa.float64()),
                "type": dict_str(p["type"]),
                "name": dict_str(p["name"]),
                "channel": pa.array(p["channel"], pa.int32()),
                "offset": pa.array(p["offset"], pa.int64()),
                "decoded": pa.array(p["decoded"], pa.string()),
                "bits": pa.array(p["bits"], pa.int64()),
                "payload": pa.array(p["payload"], pa.binary()),
            })
        return ent, pkt


#: The container's chunk kinds by number, as `type` names.
CHUNK_NAMES = {0: "header", 1: "replayData", 2: "checkpoint", 3: "event"}


def keep_container(k: Keeper, replay, buf: bytes) -> None:
    """
    The container's own items: the info block and the header (decoded into the
    match document, and kept whole since a trailer of the header is not
    read), the checkpoints and events (kept whole: a checkpoint is the state
    of every actor at its time, which the stream from the start holds too),
    and chunks of a kind not known here. Replay data chunks are counted by
    the stream that reads them.
    """
    k.meet("file.info")
    k.packet("file.info", PARTIAL, None, "file.info", replay.friendly_name, None, 0,
             {"fileVersion": replay.file_version, "lengthMs": replay.length_ms,
              "networkVersion": replay.network_version, "changelist": replay.changelist, "live": replay.live,
              "recordedUnix": replay.recorded_unix, "compressed": replay.compressed, "encrypted": replay.encrypted,
              "customVersions": replay.custom_versions},
             data=buf[: replay.info_size])
    for c in replay.chunks:
        name = CHUNK_NAMES.get(c.kind, str(c.kind))
        kind = f"chunk.{name}"
        if c.kind == 1:
            continue
        k.meet(kind)
        whole = buf[c.offset : c.offset + c.size]
        if c.kind == 0:
            h = replay.header
            k.packet(kind, PARTIAL, None, kind, "", None, c.offset,
                     {"unreadBytes": len(h.unread) if h else None}, data=whole)
        else:
            k.packet(kind, RAW, c.start_ms / 1000.0 if c.kind in (2, 3) else None, kind, c.id, None, c.offset,
                     {"id": c.id, "group": c.group, "metadata": c.metadata, "startMs": c.start_ms,
                      "endMs": c.end_ms, "dataOffset": c.data_offset, "dataSize": c.data_size}
                     if c.kind in (2, 3) else {"kind": c.kind}, data=whole)
