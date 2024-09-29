from dotenv import load_dotenv
from fastapi import FastAPI

from scpm.swarm.server import swarm as swarm_router

load_dotenv()

app = FastAPI()
app.include_router(swarm_router)


@app.get("/health", tags=["health check"])
def health():
    return {"status": "OK"}
