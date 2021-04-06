import asyncio
import uvicorn
from fastapi import FastAPI
from uvicorn import Config, Server

app = FastAPI()

@app.get("/")
async def hello(index: str):
    return f"Hello: {index}"



config = Config(app, host="127.0.0.1", port=8000, log_level="info", reload=True)
server = Server(config)

async def serve():
    return await server.serve()

# loop = asyncio.get_event_loop()
# loop.run_until_complete(serve())
asyncio.run(serve())
# uvicorn.run(app)

