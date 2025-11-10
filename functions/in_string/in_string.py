"""Lambda function to substring a string."""

__author__ = "Dave Hall <me@davehall.com.au>"
__copyright__ = "Copyright 2024, 2025, Skwashd Services Pty Ltd https://davehall.com.au"
__license__ = "MIT"

from typing import Any

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()


@logger.inject_lambda_context(log_event=True)
def handler(event: dict[str, Any], _: LambdaContext) -> dict[str, int]:
    """
    Find a substring in a string.

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
    string = event.get("string")
    string_type = type(string)
    if string_type is not str:
        logger.info("Recevied invalid string.")
        raise TypeError(f"Expected string, received {string_type} for string")  # noqa: TRY003 We don't need a custom exception class for this

    string = str(string)
    string = string.strip()
    if not string:
        logger.info("Recevied empty string.")
        raise ValueError("Received empty string")  # noqa: TRY003 We don't need a custom exception class for this

    substring = event.get("substring")
    substring_type = type(substring)
    if substring_type is not str:
        logger.info("Recevied invalid substring.")
        raise TypeError(f"Expected string, received {substring_type} for substring")  # noqa: TRY003 We don't need a custom exception class for this

    substring = str(substring)
    substring = substring.strip()
    if not substring:
        logger.info("Recevied empty substring.")
        raise ValueError("Received empty substring")  # noqa: TRY003 We don't need a custom exception class for this

    index = string.find(substring)
    response = {"index": index}

    logger.debug("Response", extra=response)

    return response
