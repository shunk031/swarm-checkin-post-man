import os
from functools import lru_cache

from scpm.config import get_configs


@lru_cache
def get_host_url() -> str:
    conf = get_configs()

    host = os.environ["SCPM_REMOTE_HOST"]
    port = conf.scpm_port

    if conf.scpm_dev_env == "development":
        return f"{host}:{port}"
    elif conf.scpm_dev_env == "production":
        return host
    else:
        raise ValueError(f"Invalid {conf.scpm_dev_env=}")
