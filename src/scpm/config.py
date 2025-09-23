from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

Environment = Literal[
    "beta",
    "real",
]


class Configs(BaseSettings):
    scpm_endpoint: str
    scpm_dev_env: Environment
    scpm_port: str

    swarm_client_id: str
    swarm_client_secret: str
    swarm_push_secret: str

    x_client_id: str
    x_client_secret: str
    x_access_token: str
    x_access_token_secret: str
    x_bearer_token: str
    x_consumer_api_key: str
    x_consumer_secret: str

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_configs() -> Configs:
    return Configs()  # type: ignore
