from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from scpm.swarm import (
    get_swarm_auth_url,
    get_swarm_push_api_url,
    get_swarm_redirect_url,
)
from scpm.swarm.server import swarm as swarm_router

app = FastAPI()
app.include_router(swarm_router)

templates = Jinja2Templates(directory="scpm/templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "redirect_url": get_swarm_redirect_url(),
            "push_api_url": get_swarm_push_api_url(),
            "auth_url": get_swarm_auth_url(),
        },
    )


@app.get("/health", tags=["health check"])
def health():
    return Response(content="OK")
