"""Lambda function to find a value in a dictionary by key."""

__author__ = "Dave Hall <me@davehall.com.au>"
__copyright__ = "Copyright 2024, 2025, Skwashd Services Pty Ltd https://davehall.com.au"
__license__ = "MIT"

from typing import Any

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()


@logger.inject_lambda_context(log_event=True)
def handler(event: dict[str, Any], _: LambdaContext) -> dict[str, str | Any | None]:
    """
    Find a value in a dictionary by key.

    Args:
    ----
        event: Event payload.
        _: AWS Lambda Context object.

    Returns:
    -------
        JSON response.

    """
    logger.warning(
        "This function is deprecated and will be removed in the future. Use JSONata instead."
    )

    values: dict[str, Any] = event.get("values")  # type: ignore[assignment]
    # JSON converts empty objects to empty lists, so we need to check for this.
    if type(values) is list and len(values) == 0:
        logger.info("Recevied empty list, instead of dictionary.")
        return {"value": None}

    key = event.get("key")
    if not key:
        logger.error("Key is missing from event body")
        raise ValueError("Key is missing from event body")  # noqa: TRY003 We don't need a custom exception class for this

    value = values.get(key)

    response = {"value": value}

    logger.debug("Response", extra=response)

    return response
