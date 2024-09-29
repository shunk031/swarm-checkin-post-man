import requests

SWARM_USERS_SELF_URL = "https://api.foursquare.com/v2/users/self"
SWARM_USERS_SELF_CHECKINS_URL = "https://api.foursquare.com/v2/users/self/checkins"
SWARM_USERS_SELF_PHOTOS_URL = "https://api.foursquare.com/v2/users/self/photos"


def fetch_latest_checkin(access_token: str, versioning: str):
    res = requests.get(
        url=SWARM_USERS_SELF_CHECKINS_URL,
        params={"v": versioning, "oauth_token": access_token, "limit": "1"},
    )
    res.raise_for_status()
    data = res.json()
    return data["response"]["checkins"]["items"][0]


def fetch_swarm_user_id_by_token(access_token: str, versioning: str):
    res = requests.get(
        url=SWARM_USERS_SELF_URL,
        params={"v": versioning, "oauth_token": access_token},
    )
    res.raise_for_status()
    data = res.json()

    return data["response"]["user"]


def fetch_latest_photo_list(access_token: str, versioning: str):
    res = requests.get(
        url=SWARM_USERS_SELF_PHOTOS_URL,
        params={"v": versioning, "oauth_token": access_token, "limit": "1"},
    )
    res.raise_for_status()
    data = res.json()

    return data["response"]["photos"]
