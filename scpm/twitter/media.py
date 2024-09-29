import io
import os
from typing import List, Optional
from urllib.parse import urlparse

import requests
import tweepy


def upload_media(v1_client: tweepy.API, checkin) -> Optional[List[str]]:
    has_photo = checkin["photos"]["count"] > 0  # type: ignore
    if not has_photo:
        return None

    photo_json = checkin["photos"]["items"][0]  # type: ignore
    photo_url = photo_json["prefix"] + "original" + photo_json["suffix"]

    res = requests.get(photo_url)
    res.raise_for_status()

    photo_img = io.BytesIO(res.content)
    photo_img.seek(0)

    filename = os.path.basename(urlparse(photo_url).path)

    media = v1_client.media_upload(filename=filename, file=photo_img)
    media_ids = [media.media_id]

    return media_ids
