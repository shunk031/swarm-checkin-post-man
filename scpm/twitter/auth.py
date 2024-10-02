import os
from dataclasses import dataclass

import tweepy

from scpm.config import get_configs


@dataclass
class TwitterClient(object):
    v1: tweepy.API
    v2: tweepy.Client


def _get_v1_client() -> tweepy.API:
    conf = get_configs()
    x_auth = tweepy.OAuthHandler(
        consumer_key=conf.x_consumer_api_key,
        consumer_secret=conf.x_consumer_secret,
        access_token=conf.x_access_token,
        access_token_secret=conf.x_access_token_secret,
    )

    x_v1_client = tweepy.API(auth=x_auth)
    x_v1_client.verify_credentials()

    return x_v1_client


def _get_v2_client() -> tweepy.Client:
    conf = get_configs()

    x_v2_client = tweepy.Client(
        bearer_token=conf.x_bearer_token,
        consumer_key=conf.x_consumer_api_key,
        consumer_secret=conf.x_consumer_secret,
        access_token=conf.x_access_token,
        access_token_secret=conf.x_access_token_secret,
    )
    return x_v2_client


def get_twitter_api_clients():
    return TwitterClient(v1=_get_v1_client(), v2=_get_v2_client())
