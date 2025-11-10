"""Convert IP address to an object."""

__author__ = "Dave Hall <me@davehall.com.au>"
__copyright__ = "Copyright 2024, 2025, Skwashd Services Pty Ltd https://davehall.com.au"
__license__ = "MIT"

import ipaddress

from aws_lambda_powertools.logging import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()


class InvalidIPError(Exception):
    """Invalid IP Address exception class."""

    message = "Invalid IP Address."


class IPInfo:
    """IP Address object."""

    def __init__(self, ip: str) -> None:
        """Initialize IP Address object."""
        self.ipaddress = ipaddress.ip_address(ip)

    def __str__(self) -> str:
        """Return IP Address as string."""
        return str(self.ipaddress)

    def __int__(self) -> int:
        """Return IP Address as integer."""
        return int(self.ipaddress)

    def to_dict(self) -> dict:
        """Convert the IP Address object to a dictionary."""
        common = {
            "int": int(self.ipaddress),
            "version": self.ipaddress.version,
            "max_prefixlen": self.ipaddress.max_prefixlen,
            "exploded": self.ipaddress.exploded,
            "packed": self.ipaddress.packed,
            "compressed": self.ipaddress.compressed,
            "reverse_pointer": self.ipaddress.reverse_pointer,
            "is_multicast": self.ipaddress.is_multicast,
            "is_private": self.ipaddress.is_private,
            "is_global": self.ipaddress.is_global,
            "is_unspecified": self.ipaddress.is_unspecified,
            "is_reserved": self.ipaddress.is_reserved,
            "is_loopback": self.ipaddress.is_loopback,
            "is_link_local": self.ipaddress.is_link_local,
        }

        if self.ipaddress.version == 4:
            return common

        ipv6_info = {
            "ipv4_mapped": self.ipaddress.ipv4_mapped,
            "scope_id": self.ipaddress.scope_id,
            "sixtofour": self.ipaddress.sixtofour,
            "teredo": self.ipaddress.teredo,
        }

        return {**common, **ipv6_info}


@logger.inject_lambda_context(log_event=True)
def handler(event: dict[str, str], _: LambdaContext) -> dict[str, str]:
    """Convert IP address to an integer."""
    if "ip" not in event:
        logger.error("IP address missing from event body")
        raise ValueError("IP address missing from event body")  # noqa: TRY003 We don't need a custom exception class for this

    try:
        response = IPInfo(event["ip"]).to_dict()
    except ValueError as e:
        logger.exception("Invalid IP Address")
        raise InvalidIPError() from e

    logger.debug("Response", extra=response)

    return response
