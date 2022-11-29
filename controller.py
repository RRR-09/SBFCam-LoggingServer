import json
import traceback
from typing import List

from models import (
    BUFFERED_DATA_REQUEST_KEYS_LEN,
    PLAYER_DATA_REQUEST_KEYS,
    PLAYER_DATA_REQUEST_KEYS_LEN,
    TEMPORAL_DATA_REQUEST_KEYS_LEN,
    BufferedDataRequest,
    DataArrayLengthMismatch,
    PlayerDataRequest,
    TemporalDataRequest,
)


async def format_data(data: List) -> BufferedDataRequest:
    """
    Converts positional list-based data to an easier-to-use dict.

    Raises an error if validation mismatches.
    """
    # TODO: Fix redundant processing, simplify assertions

    if len(data) != BUFFERED_DATA_REQUEST_KEYS_LEN:
        raise DataArrayLengthMismatch(
            model="BufferedDataRequest",
            expected_len=BUFFERED_DATA_REQUEST_KEYS_LEN,
            received_len=len(data),
        )

    server_id = data[0]
    server_version = data[1]
    timepoints = data[2]

    processed_buffer_data = []

    for timepoint in timepoints:
        if len(timepoint) != TEMPORAL_DATA_REQUEST_KEYS_LEN:
            raise DataArrayLengthMismatch(
                model="TemporalDataRequest",
                expected_len=TEMPORAL_DATA_REQUEST_KEYS_LEN,
                received_len=len(timepoint),
            )

        unix_timestamp = timepoint[0]
        temporal_data = timepoint[1]

        processed_temporal_data: List[PlayerDataRequest] = []
        for player_data in temporal_data:
            if len(player_data) != PLAYER_DATA_REQUEST_KEYS_LEN:
                raise DataArrayLengthMismatch(
                    model="PlayerDataRequest",
                    expected_len=PLAYER_DATA_REQUEST_KEYS_LEN,
                    received_len=len(player_data),
                )

            processed_player_data = PlayerDataRequest(
                **dict(zip(PLAYER_DATA_REQUEST_KEYS, player_data))
            )
            processed_temporal_data.append(processed_player_data)

        new_timepoint = TemporalDataRequest(
            unix_timestamp=unix_timestamp, player_data=processed_temporal_data
        )
        processed_buffer_data.append(new_timepoint)

    return BufferedDataRequest(
        server_id=server_id,
        server_version=server_version,
        buffered_data=processed_buffer_data,
    )


async def handle_data(data: List):
    try:
        formatted_data = await format_data(data)
    except Exception as e:
        # TODO: Better error logging
        print(f"Could not format data:\n{e}\n{data}\n{traceback.format_exc()}")
        return

    print(json.dumps(json.loads(formatted_data.json()), indent=2))
