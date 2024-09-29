import os
from dataclasses import dataclass

import tweepy


@dataclass
class TwitterClient(object):
    v1: tweepy.API
    v2: tweepy.Client


def _get_v1_client() -> tweepy.API:
    x_auth = tweepy.OAuthHandler(
        consumer_key=os.environ["X_CONSUMER_API_KEY"],
        consumer_secret=os.environ["X_CONSUMER_SECRET"],
        access_token=os.environ["X_ACCESS_TOKEN"],
        access_token_secret=os.environ["X_ACCESS_TOKEN_SECRET"],
    )

    x_v1_client = tweepy.API(auth=x_auth)
    x_v1_client.verify_credentials()

    return x_v1_client


def _get_v2_client() -> tweepy.Client:
    x_v2_client = tweepy.Client(
        bearer_token=os.environ["X_BEARER_TOKEN"],
        consumer_key=os.environ["X_CONSUMER_API_KEY"],
        consumer_secret=os.environ["X_CONSUMER_SECRET"],
        access_token=os.environ["X_ACCESS_TOKEN"],
        access_token_secret=os.environ["X_ACCESS_TOKEN_SECRET"],
    )
    return x_v2_client


def get_twitter_api_clients():
    return TwitterClient(v1=_get_v1_client(), v2=_get_v2_client())
