from functools import lru_cache
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

Environment = Literal[
    "beta",
    "real",
]


class Configs(BaseSettings):
    scpm_endpoint: str
    scpm_dev_env: Environment
    scpm_port: str

    swarm_client_id: SecretStr
    swarm_client_secret: SecretStr
    swarm_push_secret: SecretStr

    x_client_id: SecretStr
    x_client_secret: SecretStr
    x_access_token: SecretStr
    x_access_token_secret: SecretStr
    x_bearer_token: SecretStr
    x_consumer_api_key: SecretStr
    x_consumer_secret: SecretStr

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_configs() -> Configs:
    return Configs()  # type: ignore
