from typing import List
from uuid import UUID

from pydantic import BaseModel


class DataArrayLengthMismatch(ValueError):
    def __init__(self, model: str, expected_len: int, received_len: int):
        message = f"Mismatch in '{str(model)}' (Expected {expected_len}, received {received_len})"
        super().__init__(message)


class PlayerDataRequest(BaseModel):
    """Incoming datapoint, a fragment of data for a specific player"""

    player_id: int
    player_name: str
    position_x: float
    position_y: float
    position_z: float
    rotation_x: float
    rotation_y: float
    rotation_z: float
    size_x: float
    size_y: float
    size_z: float
    velocity_x: float
    velocity_y: float
    velocity_z: float
    scale_type: str
    character_type: str


class TemporalDataRequest(BaseModel):
    """Incoming datapoint, a collection of playerdata at a specific point in time"""

    unix_timestamp: float
    player_data: List[PlayerDataRequest]


class BufferedDataRequest(BaseModel):
    """Incoming datapoint, effectively the top-level formatted model.
    Server ID and version, containing a list of polled timepoints, each timepoint containing its own collection of
    playerdata collected at that time."""

    server_id: UUID
    server_version: int
    buffered_data: List[TemporalDataRequest]


# Save values so they're not manually defined/constantly calculated
PLAYER_DATA_REQUEST_KEYS = list(PlayerDataRequest.__fields__.keys())
PLAYER_DATA_REQUEST_KEYS_LEN = len(PLAYER_DATA_REQUEST_KEYS)
TEMPORAL_DATA_REQUEST_KEYS_LEN = len(TemporalDataRequest.__fields__)
BUFFERED_DATA_REQUEST_KEYS_LEN = len(BufferedDataRequest.__fields__)


class Vector3(BaseModel):
    """Basic 3-value vector"""

    x: float
    y: float
    z: float
