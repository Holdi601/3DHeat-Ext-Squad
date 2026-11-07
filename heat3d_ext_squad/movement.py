"""
The engine's own replicated types, decoded from a property's bits.

`ReplicatedMovement` is AActor's FRepMovement, the same for every Unreal game
that does not change its quantization: two flags (sleeping, physics), two more
from engine network version 25 (server frame, server physics handle), the
location as a quantized vector (two decimals by default: scale 100), the
rotation as three optional bytes, the linear velocity (whole numbers: scale
1), the angular velocity when physics is replicated, then the server frame
and handle when flagged. Checked on Squad's demos: each sample's step from
the one before matches the velocity it carries.

Squad's helicopters replicate their movement through their own movement
component with other settings; those are not decoded here.
"""

from __future__ import annotations

from dataclasses import dataclass

from .bits import BitReader, ReadError
from .stream import ENG_REP_MOVE_SERVER_FRAME, Vec, packed_vector


@dataclass
class RepMovement:
    location: Vec
    yaw: float
    pitch: float
    roll: float
    velocity: Vec
    physics: bool


def rep_movement(b: BitReader, eng: int, location_scale: float = 100.0, velocity_scale: float = 1.0) -> RepMovement:
    b.bit()  # simulated physics sleeping
    physics = b.bit()
    server_frame = server_handle = False
    if eng >= ENG_REP_MOVE_SERVER_FRAME and eng != 26:
        server_frame = b.bit()
        server_handle = b.bit()
    loc = packed_vector(b, location_scale, 30, eng)
    pitch, yaw, roll = (b.u8() * 360.0 / 256.0 if b.bit() else 0.0 for _ in range(3))
    vel = packed_vector(b, velocity_scale, 24, eng)
    if physics:
        packed_vector(b, velocity_scale, 24, eng)  # angular velocity
    if server_frame:
        b.packed()
    if server_handle:
        b.packed()
    # Squad v10.3.1 (UE 5.5) writes one more bit after these, always 0 in the
    # demos checked; what a 1 would bring is unknown, so only a 0 is accepted.
    # Any other remainder means this is not the FRepMovement layout above and
    # its numbers would be wrong.
    if b.left() == 1 and not b.bit():
        pass
    elif not b.at_end():
        raise ReadError(f"{b.left()} bits left after the movement")
    return RepMovement(loc, _signed(yaw), _signed(pitch), _signed(roll), vel, physics)


def _signed(deg: float) -> float:
    return deg - 360.0 if deg > 180.0 else deg


# Small property types, read the way FRepLayout writes them.


def string(b: BitReader) -> str:
    return b.fstring()


def int32(b: BitReader) -> int:
    return b.i32()


def object_ref(b: BitReader) -> int:
    """An object reference: its net GUID, packed (0 means none)."""
    return b.packed()
