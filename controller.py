import json
import traceback
from queue import Empty, SimpleQueue
from typing import List, cast

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

MOVEMENT_CACHE = {}


def data_processor_loop(insertion_queue: SimpleQueue):
    """
    A loop run at start that handles processing of validated entries
    """
    while True:
        try:
            item = cast(BufferedDataRequest, insertion_queue.get())
        except Empty:
            # Keep trying if we have an empty queue
            continue

        print(json.dumps(json.loads(item.json()), indent=2))


async def validate_data(data: List) -> BufferedDataRequest:
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


async def handle_data(insertion_queue: SimpleQueue, data: List):
    try:
        validated_data = await validate_data(data)
    except Exception as e:
        # TODO: Better error logging
        print(f"Could not format data:\n{e}\n{data}\n{traceback.format_exc()}")
        return

    insertion_queue.put(validated_data)
