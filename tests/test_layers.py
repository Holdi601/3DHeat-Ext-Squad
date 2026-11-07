"""The byte and bit archives and the replay container, on synthetic data."""

from __future__ import annotations

import struct

import pytest

from heat3d_ext_squad import container
from heat3d_ext_squad.bits import BitReader, ByteReader, ReadError, concat
from heat3d_ext_squad.container import DemoHeader

from writer import BitWriter, fstring, packed


# ------------------------------------------------------------------ archives


@pytest.mark.parametrize("v", [0, 1, 63, 64, 127, 128, 300, 16383, 16384, 2**31 - 1])
def test_packed_round_trip(v):
    assert ByteReader(packed(v)).packed() == v
    assert BitReader.from_bytes(packed(v)).packed() == v


def test_packed_too_long_is_refused():
    with pytest.raises(ReadError):
        ByteReader(b"\xff" * 6).packed()


@pytest.mark.parametrize("v,top", [(0, 15), (14, 15), (5, 16384), (16383, 16384), (1000, 1 << 32)])
def test_serialized_int_round_trip(v, top):
    w = BitWriter().serialized_int(v, top).bits(0b101, 3)
    r = BitReader(w.value, w.n)
    assert r.serialized_int(top) == v
    assert r.bits(3) == 0b101 and r.at_end()


def test_bits_are_lowest_first():
    r = BitReader.from_bytes(b"\x01\x80")
    assert r.bit() is True
    r.skip(14)
    assert r.bit() is True and r.at_end()


def test_fstrings_both_encodings():
    utf16 = "Grüße".encode("utf-16-le") + b"\x00\x00"
    buf = fstring("hello") + struct.pack("<i", -(len(utf16) // 2)) + utf16 + fstring("")
    r = ByteReader(buf)
    assert (r.fstring(), r.fstring(), r.fstring()) == ("hello", "Grüße", "")
    b = BitReader.from_bytes(buf)
    assert (b.fstring(), b.fstring(), b.fstring()) == ("hello", "Grüße", "")


def test_a_wild_string_length_is_refused_not_allocated():
    with pytest.raises(ReadError):
        BitReader.from_bytes(struct.pack("<i", 0x7FFFFFF0) + b"abc").fstring()


def test_reads_past_the_end_raise():
    r = BitReader.from_bytes(b"\xff", 5)
    r.bits(5)
    with pytest.raises(ReadError):
        r.bit()
    with pytest.raises(ReadError):
        ByteReader(b"\x00\x00").u32()


def test_windows_and_concatenation():
    w = BitWriter().bits(0b1101, 4).bits(0x3F, 6).bits(1, 1)
    r = BitReader(w.value, w.n)
    r.bits(4)
    win = r.window(6)
    assert r.bit() is True and r.at_end()
    assert win.bits(6) == 0x3F and win.at_end()
    joined = concat((0b101, 3), (0b11, 2))
    assert joined == (0b11101, 5)


def test_fname_hardcoded_and_plain():
    w = BitWriter().bit(True).packed(102).bit(False).fstring("FSTemplate_ABC").i32(0)
    w.bit(False).fstring("Some_Name").i32(2)
    r = BitReader(w.value, w.n)
    assert r.fname() == "#name102"
    assert r.fname() == "FSTemplate_ABC"
    assert r.fname() == "Some_Name_1"


# ----------------------------------------------------------------- container


def header(**kw) -> DemoHeader:
    h = DemoHeader(network_version=19, network_checksum=7, engine_network_version=36, game_network_version=0,
                   guid="00" * 16, engine_version=(5, 5, 4), changelist=123, branch="//Squad/v10.3.1",
                   levels=[("/Game/Maps/Test_Map/Gameplay_Layers/Test_Layer_v1", 0)], flags=0,
                   platform="LinuxServer", min_record_hz=0.0, max_record_hz=8.0)
    for k, v in kw.items():
        setattr(h, k, v)
    return h


def test_container_round_trip():
    frames = b"\x01\x02\x03"
    buf = container.build(header(), [(0, 20000, frames), (20000, 30000, b"")],
                          [("ev1", "kills", "meta", 5, 6, b"payload")],
                          length_ms=30000, friendly="my demo", recorded_unix=1775576610.5)
    f = container.read(buf)
    assert (f.file_version, f.length_ms, f.friendly_name, f.compressed, f.encrypted) == (7, 30000, "my demo", False,
                                                                                        False)
    assert abs(f.recorded_unix - 1775576610.5) < 1e-3
    assert [c.kind for c in f.chunks] == [0, 1, 1, 3]
    d = f.data_chunks()
    assert (d[0].start_ms, d[0].end_ms, d[0].data_size) == (0, 20000, 3)
    assert buf[d[0].data_offset : d[0].data_offset + d[0].data_size] == frames
    ev = f.events()[0]
    assert (ev.id, ev.group, ev.metadata, ev.start_ms) == ("ev1", "kills", "meta", 5)
    assert buf[ev.data_offset : ev.data_offset + ev.data_size] == b"payload"
    h = f.header
    assert (h.network_version, h.engine_network_version, h.engine_version, h.branch) == (19, 36, (5, 5, 4),
                                                                                         "//Squad/v10.3.1")
    assert h.levels == [("/Game/Maps/Test_Map/Gameplay_Layers/Test_Layer_v1", 0)]
    assert (h.platform, h.max_record_hz) == ("LinuxServer", 8.0)
    assert not h.streaming_fixes and not h.game_specific_frame_data


@pytest.mark.parametrize("version", [3, 4, 5, 6, 7])
def test_older_file_versions(version):
    f = container.read(container.build(header(), [(0, 10, b"abc")], file_version=version, length_ms=10))
    c = f.data_chunks()[0]
    assert c.data_size == 3 and f.length_ms == 10
    if version >= 4:
        assert c.end_ms == 10


def test_header_flags_and_older_header_versions():
    h = container.read(container.build(header(flags=2 | 8), [])).header
    assert h.streaming_fixes and h.game_specific_frame_data
    old = header(network_version=11)
    h = container.read(container.build(old, [])).header
    assert h.network_version == 11 and h.branch == "//Squad/v10.3.1" and h.guid == ""


def test_compressed_and_encrypted_are_flagged():
    f = container.read(container.build(header(), [], compressed=True, encrypted=True))
    assert f.compressed and f.encrypted


def test_wrong_magic_and_truncation():
    with pytest.raises(ReadError):
        container.read(b"\x00" * 64)
    buf = container.build(header(), [(0, 1, b"x" * 100)])
    with pytest.raises(ReadError):
        container.read(buf[:-10])


def test_header_magic_is_checked():
    with pytest.raises(ReadError):
        container.read_header(b"\x00" * 40)
