from json import JSONDecodeError
from os import getenv
from queue import SimpleQueue
from threading import Thread

from controller import data_processor_loop, handle_data
from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, Header, HTTPException, Request, status
from utils import check_dotenv

app = FastAPI(
    title="SBF - Logging Backend",
    description=(
        "HTTP server for receiving, processing, and storing log data from the game"
    ),
)


@app.on_event("startup")
async def startup_event():
    load_dotenv(".env", verbose=True)
    check_dotenv()
    app.state.auth_key = getenv("AUTH_KEY")
    app.state.insertion_queue = SimpleQueue()
    Thread(
        target=data_processor_loop, args=(app.state.insertion_queue), daemon=True
    ).start()


@app.get("/")
async def about():
    return {"message": {"title": app.title, "description": app.description}}


@app.post("/player_data")
async def post_player_data(
    request: Request,
    background_tasks: BackgroundTasks,
    x_token: str | None = Header(default=None),
):
    # TODO: Implement actual authentication
    if x_token != app.state.auth_key:
        if x_token is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No 'X-Token' header provided.",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect token.",
            )

    # Incoming data is positional, which Pydantic explicitly refuses to support.
    # We have to do things manually.
    content_type = request.headers.get("Content-Type")
    if content_type is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No 'Content-Type' header provided.",
        )
    elif content_type == "application/json":
        try:
            data_json = await request.json()
        except (JSONDecodeError, TypeError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to decode JSON body.",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to decode JSON body.",
        )

    background_tasks.add_task(handle_data, app.state.insertion_queue, data_json)

    return {"message": "Received"}
