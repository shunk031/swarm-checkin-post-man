from functools import lru_cache
from typing import Optional

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Configs(BaseSettings):
    scpm_dev_env: str
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

    ngrok_authtoken: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env")

    @field_validator("scpm_dev_env")
    def validate_scpm_dev_env(cls, value):
        if value not in ("development", "production"):
            raise ValueError(
                'scpm_dev_env must be either "development" or "production"'
            )
        return value


@lru_cache
def get_configs() -> Configs:
    return Configs()  # type: ignore
