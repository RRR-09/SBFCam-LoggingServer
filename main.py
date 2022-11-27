from json import JSONDecodeError
from os import getenv

import utils
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Request, status

app = FastAPI(
    title="SBF - Logging Backend",
    description=(
        "HTTP server for receiving, processing, and storing log data from the game"
    ),
)


@app.on_event("startup")
async def startup_event():
    load_dotenv(".env", verbose=True)
    utils.check_dotenv()
    app.state.auth_key = getenv("AUTH_KEY")


@app.get("/")
async def about():
    return {"message": {"title": app.title, "description": app.description}}


@app.post("/player_data")
async def post_player_data(
    request: Request, x_token: str | None = Header(default=None)
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
        except JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to decode JSON body.",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to decode JSON body.",
        )

    print(data_json)
    return {"message": "Received"}
