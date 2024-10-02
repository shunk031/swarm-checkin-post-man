import os
from contextlib import asynccontextmanager

import ngrok
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from loguru import logger

from scpm.config import get_configs
from scpm.swarm import (
    get_swarm_auth_url,
    get_swarm_push_api_url,
    get_swarm_redirect_url,
)
from scpm.swarm.server import swarm as swarm_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    def set_scpm_host(host: str, env_key: str = "SCPM_REMOTE_HOST"):
        logger.info(f"Setting env var `{env_key}` to {host}")
        os.environ[env_key] = host

    def display_swarm_info():
        auth_url = get_swarm_auth_url()

        logger.warning(
            f"Please authenticate Swarm by accessing the following URL: {auth_url}"
        )

        logger.debug(
            "Note that the following URLs should be set in Foursquare Developer Console "
            "(https://ja.foursquare.com/developers/home):"
        )
        logger.debug(f"[Auth] Redirect URL: {get_swarm_redirect_url()}")
        logger.debug(f"[Push] Push API URL: {get_swarm_push_api_url()}")

    conf = get_configs()

    if conf.scpm_dev_env == "development":
        set_scpm_host(host="http://localhost")
        display_swarm_info()
        yield

    elif conf.scpm_dev_env == "production":
        logger.info("Setting up Ngrok Tunnel")
        ngrok.set_auth_token(conf.ngrok_authtoken)  # type: ignore

        listener = await ngrok.forward(  # type: ignore
            addr=f"localhost:{conf.scpm_port}",
        )
        ngrok_url = listener.url()
        logger.info(f"Ingress established at {ngrok_url}")

        set_scpm_host(host=ngrok_url)
        display_swarm_info()

        yield
        logger.info("Tearing Down Ngrok Tunnel")
        ngrok.disconnect()

    else:
        raise ValueError(f"Invalid {conf.scpm_dev_env=}")


app = FastAPI(lifespan=lifespan)
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
    return {"status": "OK"}
