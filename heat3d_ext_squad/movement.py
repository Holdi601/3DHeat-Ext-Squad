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
    sleeping: bool = False
    angular: Vec | None = None
    server_frame: int | None = None
    server_handle: int | None = None

    def as_dict(self) -> dict:
        """Every field, for the sidecar."""
        out = {"location": [self.location.x, self.location.y, self.location.z], "pitch": self.pitch, "yaw": self.yaw,
               "roll": self.roll, "velocity": [self.velocity.x, self.velocity.y, self.velocity.z],
               "physics": self.physics, "sleeping": self.sleeping}
        if self.angular is not None:
            out["angularVelocity"] = [self.angular.x, self.angular.y, self.angular.z]
        if self.server_frame is not None:
            out["serverFrame"] = self.server_frame
        if self.server_handle is not None:
            out["serverHandle"] = self.server_handle
        return out


def rep_movement(b: BitReader, eng: int, location_scale: float = 100.0, velocity_scale: float = 1.0) -> RepMovement:
    sleeping = b.bit()  # simulated physics sleeping
    physics = b.bit()
    server_frame = server_handle = False
    if eng >= ENG_REP_MOVE_SERVER_FRAME and eng != 26:
        server_frame = b.bit()
        server_handle = b.bit()
    loc = packed_vector(b, location_scale, 30, eng)
    pitch, yaw, roll = (b.u8() * 360.0 / 256.0 if b.bit() else 0.0 for _ in range(3))
    vel = packed_vector(b, velocity_scale, 24, eng)
    angular = packed_vector(b, velocity_scale, 24, eng) if physics else None
    frame = b.packed() if server_frame else None
    handle = b.packed() if server_handle else None
    # Squad v10.3.1 (UE 5.5) writes one more bit after these, always 0 in the
    # demos checked; what a 1 would bring is unknown, so only a 0 is accepted.
    # Any other remainder means this is not the FRepMovement layout above and
    # its numbers would be wrong.
    if b.left() == 1 and not b.bit():
        pass
    elif not b.at_end():
        raise ReadError(f"{b.left()} bits left after the movement")
    return RepMovement(loc, _signed(yaw), _signed(pitch), _signed(roll), vel, physics, sleeping, angular, frame, handle)


def helicopter_movement(b: BitReader) -> tuple[RepMovement, float]:
    """
    A Squad helicopter's movement, as its `SQHelicopterMovementComponent`
    replicates it in `ReplicatedMovement`, and the server's clock (seconds)
    it was taken at. No flags: the location (scale 100: centimetres to two
    decimals), the linear velocity (scale 100) and the angular velocity
    (scale 100, unit not checked) as quantized vectors, the rotation as
    three optional 16-bit angles (pitch, yaw, roll), then the clock as a
    32-bit float.

    Read off Squad v10.3.1 demos and checked there: every sample of five
    helicopters fills its bits exactly; a parked helicopter's location and
    yaw are its spawn's; the step between samples over the clock's step is
    the velocity (median ratio 0.997 in flight); the clock steps as the
    demo's time does (median 0.4 ms apart).
    """
    loc = packed_vector(b, 100.0, 30, 36)
    vel = packed_vector(b, 100.0, 30, 36)
    ang = packed_vector(b, 100.0, 30, 36)
    pitch, yaw, roll = (b.u16() * 360.0 / 65536.0 if b.bit() else 0.0 for _ in range(3))
    clock = b.f32()
    if not b.at_end():
        raise ReadError(f"{b.left()} bits left after the helicopter's movement")
    return RepMovement(loc, _signed(yaw), _signed(pitch), _signed(roll), vel, True, False, ang), clock


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
