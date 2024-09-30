import os
from functools import lru_cache
from typing import Final
from urllib.parse import urlencode

import requests

from scpm.config import get_configs

SWARM_AUTH_URL: Final[str] = "https://foursquare.com/oauth2/authenticate"
SWARM_ACCESS_TOKEN_URL: Final[str] = "https://foursquare.com/oauth2/access_token"


def get_swarm_auth_url(redirect_uri: str) -> str:
    conf = get_configs()

    params = {
        "client_id": conf.swarm_client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
    }
    auth_url = f"{SWARM_AUTH_URL}?{urlencode(params)}"
    return auth_url


def get_swarm_access_token(code: str, redirect_uri: str) -> str:
    conf = get_configs()

    res = requests.get(
        url=SWARM_ACCESS_TOKEN_URL,
        params={
            "client_id": conf.swarm_client_id,
            "client_secret": conf.swarm_client_secret,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
            "code": code,
        },
    )
    res.raise_for_status()

    data = res.json()
    return data["access_token"]
