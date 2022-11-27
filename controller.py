import json
import uuid
from typing import List

from models import BufferedData, PlayerData, TemporalData, Vector3


async def format_data(data: List) -> BufferedData:
    """
    Converts positional list-based data to an easier-to-use dict.

    Raises an error if validation mistmatches.
    """
    # TODO: Fix redundant processing, simplify assertions
    assert len(data) == 3

    server_id = data[0]
    server_id = uuid.UUID(str(server_id))

    server_version = data[1]
    server_version = int(server_version)

    buffered_data = data[2]
    assert isinstance(buffered_data, list)

    formatted_buffered_data = BufferedData(
        server_id=server_id, server_version=server_version, buffered_data=[]
    )
    for timepoint in buffered_data:
        timestamp = timepoint[0]
        timestamp = float(timestamp)

        temporal_data = timepoint[1]
        assert isinstance(timepoint, list)

        formatted_temporal_data = []
        for _ in range(len(temporal_data)):
            player_data = temporal_data.pop(0)
            assert len(player_data) == 13

            player_id = player_data[0]
            player_id = int(player_id)

            player_name = str(player_data[1])
            assert len(player_name) > 0

            position = {"x": player_data[2], "y": player_data[3], "z": player_data[4]}
            position["x"] = float(position["x"])
            position["y"] = float(position["y"])
            position["z"] = float(position["z"])

            rotation = {"x": player_data[5], "y": player_data[6], "z": player_data[7]}
            rotation["x"] = float(rotation["x"])
            rotation["y"] = float(rotation["y"])
            rotation["z"] = float(rotation["z"])

            size = {"x": player_data[8], "y": player_data[9], "z": player_data[10]}
            size["x"] = float(size["x"])
            size["y"] = float(size["y"])
            size["z"] = float(size["z"])

            velocity = {"x": player_data[8], "y": player_data[9], "z": player_data[10]}
            velocity["x"] = float(velocity["x"])
            velocity["y"] = float(velocity["y"])
            velocity["z"] = float(velocity["z"])

            scaleType = player_data[11]
            scaleType = str(scaleType)
            characterType = player_data[12]
            characterType = str(characterType)

            formatted_temporal_data.append(
                PlayerData(
                    player_id=player_id,
                    player_name=player_name,
                    position=Vector3.parse_obj(position),
                    rotation=Vector3.parse_obj(rotation),
                    size=Vector3.parse_obj(size),
                    velocity=Vector3.parse_obj(velocity),
                    scaleType=scaleType,
                    characterType=characterType,
                )
            )

        new_timepoint = TemporalData(
            unix_timestamp=timestamp, player_data=formatted_temporal_data
        )
        formatted_buffered_data.buffered_data.append(new_timepoint)

    return formatted_buffered_data


async def handle_data(data: List):
    try:
        formatted_data = await format_data(data)
    except Exception as e:
        print(f"Could not format data:\n{e}")
        return

    print(json.loads(formatted_data.json(), indent=2))
