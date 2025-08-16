from urllib.parse import urljoin

import requests

SWARM_CHECKINS_URL = "https://api.foursquare.com/v2/checkins/"


def fetch_swarm_share_url(access_token: str, checkin_id: str, versioning: str):
    checkin_id_url = urljoin(SWARM_CHECKINS_URL, checkin_id)
    res = requests.get(
        url=checkin_id_url,
        params={"v": versioning, "oauth_token": access_token},
    )
    res.raise_for_status()
    data = res.json()

    return data["response"]["checkin"]["checkinShortUrl"]
