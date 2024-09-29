import os
from urllib.parse import urlencode

import requests

SWARM_AUTH_URL = "https://foursquare.com/oauth2/authenticate"
SWARM_ACCESS_TOKEN_URL = "https://foursquare.com/oauth2/access_token"


def get_swarm_auth_url(redirect_uri: str) -> str:
    swarm_client_id = os.environ["SWARM_CLIENT_ID"]

    params = {
        "client_id": swarm_client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
    }
    auth_url = f"{SWARM_AUTH_URL}?{urlencode(params)}"
    return auth_url


def get_swarm_access_token(code: str, redirect_uri: str) -> str:
    swarm_client_id = os.environ["SWARM_CLIENT_ID"]
    swarm_client_secret = os.environ["SWARM_CLIENT_SECRET"]

    res = requests.get(
        url=SWARM_ACCESS_TOKEN_URL,
        params={
            "client_id": swarm_client_id,
            "client_secret": swarm_client_secret,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
            "code": code,
        },
    )
    res.raise_for_status()

    data = res.json()
    return data["access_token"]
