"""
Writers that mirror the readers, for building synthetic replays in tests.

They follow the engine's layouts as the readers do; a test that writes a value
and reads it back proves the two agree, and the real-demo tests prove the
readers agree with Squad.
"""

from __future__ import annotations

import struct


class BitWriter:
    def __init__(self) -> None:
        self.value = 0
        self.n = 0

    def bits(self, v: int, n: int) -> "BitWriter":
        self.value |= (v & ((1 << n) - 1)) << self.n
        self.n += n
        return self

    def bit(self, b: bool) -> "BitWriter":
        return self.bits(int(bool(b)), 1)

    def bytes(self, data: bytes) -> "BitWriter":
        for c in data:
            self.bits(c, 8)
        return self

    def u32(self, v: int) -> "BitWriter":
        return self.bits(v, 32)

    def i32(self, v: int) -> "BitWriter":
        return self.bits(v & 0xFFFFFFFF, 32)

    def packed(self, v: int) -> "BitWriter":
        return self.bytes(packed(v))

    def fstring(self, s: str) -> "BitWriter":
        return self.bytes(fstring(s))

    def serialized_int(self, v: int, max_value: int) -> "BitWriter":
        # FBitWriter::SerializeInt: bits, lowest first, while value + mask < max.
        written = 0
        mask = 1
        while written + mask < max_value:
            if v & mask:
                self.bit(True)
                written |= mask
            else:
                self.bit(False)
            mask <<= 1
        return self

    def f32(self, v: float) -> "BitWriter":
        return self.bytes(struct.pack("<f", v))

    def f64(self, v: float) -> "BitWriter":
        return self.bytes(struct.pack("<d", v))

    def append(self, other: "BitWriter") -> "BitWriter":
        return self.bits(other.value, other.n)

    def packet(self) -> bytes:
        """The bits with the end marker after them, padded to whole bytes."""
        n = self.n + 1
        v = self.value | (1 << self.n)
        return v.to_bytes((n + 7) // 8, "little")

    def to_bytes(self) -> bytes:
        return self.value.to_bytes((self.n + 7) // 8, "little")


def packed(v: int) -> bytes:
    out = bytearray()
    while True:
        b = (v & 0x7F) << 1
        v >>= 7
        if v:
            out.append(b | 1)
        else:
            out.append(b)
            return bytes(out)


def fstring(s: str) -> bytes:
    if not s:
        return struct.pack("<i", 0)
    raw = s.encode("utf-8") + b"\x00"
    return struct.pack("<i", len(raw)) + raw


def quantized_vector(w: BitWriter, xyz: tuple[float, float, float], scale: float, bits: int = 20) -> None:
    """WriteQuantizedVector (engine network version 23+): 7-bit header, then scaled integers."""
    w.serialized_int(bits | (1 << 6), 1 << 7)
    for c in xyz:
        w.bits(round(c * scale) & ((1 << bits) - 1), bits)


def rep_movement(xyz, yaw_byte: int, vel=(0.0, 0.0, 0.0)) -> BitWriter:
    """An FRepMovement the way Squad v10.3.1 writes it, trailing zero bit included."""
    w = BitWriter()
    w.bit(False).bit(False)  # sleeping, physics
    w.bit(False).bit(False)  # server frame, server handle
    quantized_vector(w, xyz, 100.0)
    w.bit(False)  # pitch
    w.bit(True).bits(yaw_byte, 8)
    w.bit(False)  # roll
    quantized_vector(w, vel, 1.0)
    w.bit(False)
    return w


def helicopter_movement(xyz, yaw_deg: float, vel=(0.0, 0.0, 0.0), clock: float = 0.0) -> BitWriter:
    """A Squad helicopter movement component's ReplicatedMovement, as v10.3.1 writes it."""
    w = BitWriter()
    quantized_vector(w, xyz, 100.0, 24)
    quantized_vector(w, vel, 100.0, 20)
    quantized_vector(w, (0.0, 0.0, 0.0), 100.0, 1)
    w.bit(False)  # pitch
    w.bit(True).bits(round(yaw_deg * 65536 / 360) & 0xFFFF, 16)
    w.bit(False)  # roll
    return w.f32(clock)
