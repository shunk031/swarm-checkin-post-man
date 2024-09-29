import logging
import re
import textwrap

logger = logging.getLogger("uvicorn")


def get_photo_data(photo_json):
    breakpoint()


def get_post_address(formatted_addresses) -> str:
    def re_format_post_address(address):
        return " ".join(address.split())

    if not re.match(r"\d{3}-?\d{4}", formatted_addresses[-1]):
        format_address = formatted_addresses[-1]
    else:
        format_address = formatted_addresses[-2]

    post_address = re_format_post_address(format_address)
    logger.info(formatted_addresses)

    return post_address


def construct_post_message(checkin, checkin_short_url: str) -> str:
    post_address = get_post_address(
        formatted_addresses=checkin["venue"]["location"]["formattedAddress"]  # type: ignore
    )

    has_shout = "shout" in checkin

    if has_shout:
        msg = f"""\
        {checkin['shout']} (@ {checkin['venue']['name']} in {post_address})
        {checkin_short_url}
        """
    else:
        msg = f"""\
        I'm at {checkin['venue']['name']} in {post_address}
        {checkin_short_url}
        """

    msg = textwrap.dedent(msg)
    logger.info(msg)

    return msg
