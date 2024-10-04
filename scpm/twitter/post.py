import re
import textwrap
from dataclasses import dataclass
from typing import Any, Dict

from loguru import logger


@dataclass
class PostConstructor(object):
    checkin: Dict[str, Any]
    checkin_short_url: str

    _max_num_chars: int = 140
    _num_chars_threshold: float = 0.98

    @property
    def max_num_chars(self) -> int:
        # en: len() cannot accurately count the number of characters (e.g., emojis, Unicode),
        # here the maximum number of characters is calculated considering the threshold.
        return int(self._max_num_chars * self._num_chars_threshold)

    def get_post_address(self) -> str:
        def re_format_post_address(address):
            return " ".join(address.split())

        formatted_addresses = self.checkin["venue"]["location"]["formattedAddress"]

        if not re.match(r"\d{3}-?\d{4}", formatted_addresses[-1]):
            format_address = formatted_addresses[-1]
        else:
            format_address = formatted_addresses[-2]

        post_address = re_format_post_address(format_address)
        logger.info(f"Post Address: {post_address}")

        return post_address

    def __call__(self) -> str:
        post_address = self.get_post_address()

        has_shout = "shout" in self.checkin

        if has_shout:
            half_1 = self.checkin["shout"]
            half_2 = f"(@ {self.checkin['venue']['name']} in {post_address})"
            msg = f"{half_1} {half_2}"
            num_chars = len(msg)

            if num_chars > self.max_num_chars:
                cdot = "..."
                half_1 = half_1[: self.max_num_chars - len(half_2) - 1 - len(cdot)]
                msg = f"{half_1}{cdot} {half_2}"

                # Since len() cannot accurately count the number of characters (e.g., emojis, Unicode),
                # an error is issued if the number of characters exceeds the threshold.
                assert len(msg) <= self.max_num_chars, len(msg)

        else:
            msg = f"I'm at {self.checkin['venue']['name']} in {post_address}"

        logger.debug(f"# of chars w/o URL: {len(msg)}")
        msg = textwrap.dedent(
            f"""\
            {msg}
            {self.checkin_short_url}"""
        )
        logger.debug(f"# of chars w/ URL: {len(msg)}")
        logger.debug(msg)

        return msg
