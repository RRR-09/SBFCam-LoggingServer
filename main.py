from fastapi import FastAPI

app = FastAPI(
    title="SBF - Logging Backend",
    description=(
        "HTTP server for receiving, processing, and storing log data from the game"
    ),
)


@app.get("/")
async def about():
    return {"message": {"title": app.title, "description": app.description}}


@app.post("/player_data")
async def post_player_data(test):
    print(test)
    return {"message": "Hello World"}
