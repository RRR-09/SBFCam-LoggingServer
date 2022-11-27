from typing import List
from uuid import UUID

from pydantic import BaseModel


class Vector3(BaseModel):
    """Basic 3-value vector"""

    x: float
    y: float
    z: float


class PlayerData(BaseModel):
    """Incoming datapoint, a fragment of data for a specific player"""

    player_id: int
    player_name: str
    position: Vector3
    rotation: Vector3
    size: Vector3
    velocity: Vector3
    scaleType: str
    characterType: str


class TemporalData(BaseModel):
    """Incoming datapoint, a collection of playerdata at a specific point in time"""

    unix_timestamp: float
    player_data: List[PlayerData]


class BufferedData(BaseModel):
    """Incoming datapoint, effectively the top-level formatted model.
    Server ID and version, containing a list of polled timepoints, each timepoint containing its own collection of
    playerdata collected at that time."""

    server_id: UUID
    server_version: int
    buffered_data: List[TemporalData]
