"""
Readers for the two archive kinds an Unreal replay uses.

The replay file and each frame inside it are byte archives (`ByteReader`):
little-endian integers, length-prefixed strings, Unreal's packed integers.
The network packets inside a frame are bit streams (`BitReader`), written the
way Unreal's FBitWriter writes them: the first bit is the lowest bit of the
first byte. Holding a packet as one Python integer makes that order the
integer's own bit order, so reading n bits is a shift and a mask.

Every read past the end raises `ReadError`; a reader that guessed on would
turn a damaged packet into confident nonsense.
"""

from __future__ import annotations

import struct


class ReadError(ValueError):
    """A read ran past the end of its archive, or met a value that cannot be right."""


#: The longest string accepted; a longer length means the reader is misaligned.
MAX_STRING = 1 << 20


def _decode_fstring(raw: bytes, utf16: bool) -> str:
    if utf16:
        return raw.decode("utf-16-le", errors="replace").rstrip("\x00")
    return raw.decode("utf-8", errors="replace").rstrip("\x00")


class ByteReader:
    """A byte archive over `buf[start:end]`."""

    __slots__ = ("buf", "pos", "end")

    def __init__(self, buf: bytes, start: int = 0, end: int | None = None):
        self.buf = buf
        self.pos = start
        self.end = len(buf) if end is None else end

    def left(self) -> int:
        return self.end - self.pos

    def _take(self, n: int) -> int:
        if n < 0 or self.pos + n > self.end:
            raise ReadError(f"read of {n} bytes at {self.pos} runs past {self.end}")
        at = self.pos
        self.pos += n
        return at

    def bytes(self, n: int) -> bytes:
        at = self._take(n)
        return self.buf[at : at + n]

    def skip(self, n: int) -> None:
        self._take(n)

    def u8(self) -> int:
        return self.buf[self._take(1)]

    def u16(self) -> int:
        return struct.unpack_from("<H", self.buf, self._take(2))[0]

    def u32(self) -> int:
        return struct.unpack_from("<I", self.buf, self._take(4))[0]

    def i32(self) -> int:
        return struct.unpack_from("<i", self.buf, self._take(4))[0]

    def u64(self) -> int:
        return struct.unpack_from("<Q", self.buf, self._take(8))[0]

    def i64(self) -> int:
        return struct.unpack_from("<q", self.buf, self._take(8))[0]

    def f32(self) -> float:
        return struct.unpack_from("<f", self.buf, self._take(4))[0]

    def packed(self) -> int:
        """Unreal's SerializeIntPacked: 7 bits a byte, the lowest bit says another byte follows."""
        value = 0
        shift = 0
        while True:
            b = self.u8()
            value |= (b >> 1) << shift
            if not b & 1:
                return value
            shift += 7
            if shift > 35:
                raise ReadError("packed integer longer than five bytes")

    def fstring(self) -> str:
        """An FString: int32 length with terminator; negative means UTF-16 characters."""
        n = self.i32()
        if n == 0:
            return ""
        utf16 = n < 0
        size = -n * 2 if utf16 else n
        if size > MAX_STRING:
            raise ReadError(f"string of {size} bytes")
        return _decode_fstring(self.bytes(size), utf16)


class BitReader:
    """
    A bit archive: `value` holds the bits, `pos` and `end` are bit offsets.

    Windows share the integer; `window(n)` returns a reader over the next n
    bits and moves this one past them.
    """

    __slots__ = ("value", "pos", "end")

    def __init__(self, value: int, end: int, pos: int = 0):
        self.value = value
        self.pos = pos
        self.end = end

    @classmethod
    def from_bytes(cls, data: bytes, bits: int | None = None) -> "BitReader":
        return cls(int.from_bytes(data, "little"), len(data) * 8 if bits is None else bits)

    def left(self) -> int:
        return self.end - self.pos

    def at_end(self) -> bool:
        return self.pos >= self.end

    def bits(self, n: int) -> int:
        if n < 0 or self.pos + n > self.end:
            raise ReadError(f"read of {n} bits at {self.pos} runs past {self.end}")
        v = (self.value >> self.pos) & ((1 << n) - 1)
        self.pos += n
        return v

    def bit(self) -> bool:
        if self.pos >= self.end:
            raise ReadError("read past the end")
        v = (self.value >> self.pos) & 1
        self.pos += 1
        return bool(v)

    def skip(self, n: int) -> None:
        if n < 0 or self.pos + n > self.end:
            raise ReadError(f"skip of {n} bits at {self.pos} runs past {self.end}")
        self.pos += n

    def window(self, n: int) -> "BitReader":
        """A reader over the next `n` bits; this reader moves past them."""
        if n < 0 or self.pos + n > self.end:
            raise ReadError(f"window of {n} bits at {self.pos} runs past {self.end}")
        w = BitReader(self.value, self.pos + n, self.pos)
        self.pos += n
        return w

    def rest(self) -> tuple[int, int]:
        """The remaining bits as (value, count), shifted down to start at bit 0."""
        n = self.left()
        return (self.value >> self.pos) & ((1 << n) - 1), n

    def bytes(self, n: int) -> bytes:
        return self.bits(n * 8).to_bytes(n, "little")

    def u8(self) -> int:
        return self.bits(8)

    def u16(self) -> int:
        return self.bits(16)

    def u32(self) -> int:
        return self.bits(32)

    def i32(self) -> int:
        v = self.bits(32)
        return v - (1 << 32) if v & 0x80000000 else v

    def u64(self) -> int:
        return self.bits(64)

    def f32(self) -> float:
        return struct.unpack("<f", self.bits(32).to_bytes(4, "little"))[0]

    def f64(self) -> float:
        return struct.unpack("<d", self.bits(64).to_bytes(8, "little"))[0]

    def serialized_int(self, max_value: int) -> int:
        """
        FBitReader::SerializeInt: bits, lowest first, while value + mask stays below max_value.

        The number of bits read depends on the bits themselves - a value whose
        high bits would pass max_value stops early.
        """
        value = 0
        mask = 1
        while value + mask < max_value:
            if self.bit():
                value |= mask
            mask <<= 1
        return value

    def packed(self) -> int:
        """SerializeIntPacked, read as whole bytes from the bit stream."""
        value = 0
        shift = 0
        while True:
            b = self.bits(8)
            value |= (b >> 1) << shift
            if not b & 1:
                return value
            shift += 7
            if shift > 35:
                raise ReadError("packed integer longer than five bytes")

    def fstring(self) -> str:
        n = self.i32()
        if n == 0:
            return ""
        utf16 = n < 0
        size = -n * 2 if utf16 else n
        if size > MAX_STRING or size * 8 > self.left():
            raise ReadError(f"string of {size} bytes with {self.left() // 8} left")
        return _decode_fstring(self.bytes(size), utf16)

    def fname(self) -> str:
        """
        A network FName: a bit for "hardcoded", then the engine's name index,
        or the string and its number.
        """
        if self.bit():
            return f"#name{self.packed()}"
        name = self.fstring()
        number = self.i32()
        return f"{name}_{number - 1}" if number > 0 else name


def concat(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    """Two bit strings (value, count) joined: a's bits first."""
    return a[0] | (b[0] << a[1]), a[1] + b[1]
