import asyncio
import uvicorn
from fastapi import FastAPI
from uvicorn import Config, Server

app = FastAPI()

@app.get("/")
def read_root(name: str):
    return {f"Hello {name}"}


def start_server():
    config = Config(app, host="127.0.0.1", port=8003, log_level="info", reload=True)
    server = Server(config)
    return asyncio.create_task(server.serve())
