from functools import lru_cache

from scpm.utils import get_host_url


@lru_cache
def get_swarm_redirect_url() -> str:
    return f"{get_host_url()}/swarm/callback"


@lru_cache
def get_swarm_push_api_url() -> str:
    return f"{get_host_url()}/swarm/push"
