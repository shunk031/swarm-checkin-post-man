import os
import re
import textwrap
from functools import lru_cache

from loguru import logger

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


def get_post_address(formatted_addresses) -> str:
    def re_format_post_address(address):
        return " ".join(address.split())

    if not re.match(r"\d{3}-?\d{4}", formatted_addresses[-1]):
        format_address = formatted_addresses[-1]
    else:
        format_address = formatted_addresses[-2]

    post_address = re_format_post_address(format_address)
    logger.info(f"Post Address: {post_address}")

    return post_address


def construct_post_message(checkin, checkin_short_url: str) -> str:
    post_address = get_post_address(
        formatted_addresses=checkin["venue"]["location"]["formattedAddress"]  # type: ignore
    )

    has_shout = "shout" in checkin

    if has_shout:
        msg = f"""\
        {checkin['shout']} (@ {checkin['venue']['name']} in {post_address})
        {checkin_short_url}"""
    else:
        msg = f"""\
        I'm at {checkin['venue']['name']} in {post_address}
        {checkin_short_url}"""

    msg = textwrap.dedent(msg)
    logger.debug(msg)

    return msg
