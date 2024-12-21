"""Convert an ISO 8601 datetime string to a unix timestamp."""

import datetime

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()


def isoformat_to_timestamp(isoformat: str) -> int:
    """
    Convert an ISO 8601 datetime string to a unix timestamp.

    Args:
    ----
        isoformat: ISO 8601 datetime string.

    Returns:
    -------
        int: Unix timestamp.

    """
    logger.warning(
        "This function is deprecated and will be removed in the future. Use JSONata instead."
    )
    if not isoformat:
        isoformat = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()

    timestamp = datetime.datetime.fromisoformat(isoformat)

    return int(timestamp.timestamp())


@logger.inject_lambda_context(log_event=True)
def handler(event: dict, _: LambdaContext) -> dict[str:str]:
    """
    Return a unix timestamp from an ISO 8601 datetime string.

    If the ISO 8601 datetime string is not provided, the current time is used.

    Args:
    ----
        event: Event payload.
        _: LambdaContext: AWS Lambda Context object.

    Returns:
    -------
        str: JSON response.

    """
    isoformat = event.get("isoformat")

    response = {
        "timestamp": isoformat_to_timestamp(isoformat),
    }

    logger.debug("Response", extra=response)

    return response
