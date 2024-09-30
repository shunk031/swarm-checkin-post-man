import json
import time
from typing import Final, Optional

from fastapi import APIRouter, Form
from fastapi.responses import RedirectResponse
from loguru import logger
from typing_extensions import Annotated

from scpm.config import get_configs
from scpm.twitter.auth import get_twitter_api_clients
from scpm.twitter.media import upload_media
from scpm.utils import construct_post_message

from . import get_swarm_redirect_url
from .checkins import fetch_swarm_share_url
from .oauth2 import get_swarm_access_token, get_swarm_auth_url
from .users import fetch_latest_checkin

SWARM_VERSIONING: Final[str] = "20240831"

ACCESS_TOKEN: Optional[str] = None
DELAY_FOR_WAITING_PHOTO_UPLOADING: Final[int] = 15


swarm = APIRouter(prefix="/swarm", tags=["swarm"])


@swarm.get("/auth", response_class=RedirectResponse)
async def auth():
    auth_url = get_swarm_auth_url(
        redirect_uri=get_swarm_redirect_url(),
    )
    return RedirectResponse(url=auth_url)


@swarm.get("/callback")
async def callback(code: str):
    access_token = get_swarm_access_token(
        code=code,
        redirect_uri=get_swarm_redirect_url(),
    )

    global ACCESS_TOKEN
    ACCESS_TOKEN = access_token
    logger.debug(f"Set {ACCESS_TOKEN=}")

    return {"status": "ok"}


@swarm.post("/push")
async def recieve_swarm_push(
    checkin: Annotated[str, Form()],
    user: Annotated[str, Form()],
    secret: Annotated[str, Form()],
):
    conf = get_configs()

    assert secret == conf.swarm_push_secret
    assert ACCESS_TOKEN is not None

    logger.info(
        f"Waiting for {DELAY_FOR_WAITING_PHOTO_UPLOADING} seconds for photo uploading"
    )
    time.sleep(DELAY_FOR_WAITING_PHOTO_UPLOADING)

    checkin_json = json.loads(checkin)
    checkin_id = checkin_json["id"]

    checkin = fetch_latest_checkin(
        access_token=ACCESS_TOKEN,
        versioning=SWARM_VERSIONING,
    )
    assert checkin["id"] == checkin_id  # type: ignore

    share_url = fetch_swarm_share_url(
        access_token=ACCESS_TOKEN,
        checkin_id=checkin_id,
        versioning=SWARM_VERSIONING,
    )

    post_message = construct_post_message(
        checkin=checkin,
        checkin_short_url=share_url,
    )

    client = get_twitter_api_clients()

    media_ids = upload_media(
        v1_client=client.v1,
        checkin=checkin,
    )
    client.v2.create_tweet(
        text=post_message,
        media_ids=media_ids,
    )
