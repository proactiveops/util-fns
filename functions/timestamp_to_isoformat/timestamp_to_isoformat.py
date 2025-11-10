"""Convert a unix timestamp to an ISO 8601 datetime string."""

__author__ = "Dave Hall <me@davehall.com.au>"
__copyright__ = "Copyright 2024, 2025, Skwashd Services Pty Ltd https://davehall.com.au"
__license__ = "MIT"

import datetime

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()


def timestamp_to_isoformat(timestamp: str | float | None) -> str:
    """
    Convert an ISO 8601 datetime string to a unix timestamp.

    Args:
    ----
        timestamp: Unix timestamp.

    Returns:
    -------
        ISO 8601 datetime string.

    """
    logger.warning(
        "This function is deprecated and will be removed in the future. Use JSONata instead."
    )
    if not timestamp:
        timestamp = datetime.datetime.now(tz=datetime.UTC).timestamp()

    timestamp = float(timestamp)

    return datetime.datetime.fromtimestamp(timestamp, tz=datetime.UTC).isoformat()


@logger.inject_lambda_context(log_event=True)
def handler(event: dict, _: LambdaContext) -> dict[str, str]:
    """
    Return an ISO 8601 datetime string from a unix timestamp.

    If the timestamp is not provided, the current time is used.

    Args:
    ----
        event: Event payload.
        _: LambdaContext: AWS Lambda Context object.

    Returns:
    -------
        JSON response.

    """
    timestamp = event.get("timestamp")

    response = {
        "isoformat": timestamp_to_isoformat(timestamp),
    }

    logger.debug("Response", exatra=response)

    return response
