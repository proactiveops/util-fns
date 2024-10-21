"""Lambda function to substring a string."""

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()


@logger.inject_lambda_context(log_event=True)
def handler(event: dict[str, any], _: LambdaContext) -> dict[str, str]:
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
    string = event.get("string")
    string_type = type(string)
    if string_type is not str:
        logger.info("Recevied invalid string.")
        raise TypeError(f"Expected string, received {string_type} for string")  # noqa: TRY003 We don't need a custom exception class for this

    string = string.strip()
    if not string:
        logger.info("Recevied empty string.")
        raise ValueError("Received empty string")  # noqa: TRY003 We don't need a custom exception class for this

    substring = event.get("substring")
    substring_type = type(substring)
    if substring_type is not str:
        logger.info("Recevied invalid substring.")
        raise TypeError(f"Expected string, received {substring_type} for substring")  # noqa: TRY003 We don't need a custom exception class for this

    substring = substring.strip()
    if not substring:
        logger.info("Recevied empty substring.")
        raise ValueError("Received empty substring")  # noqa: TRY003 We don't need a custom exception class for this

    index = string.find(substring)
    response = {"index": index}

    logger.debug("Response", extra=response)

    return response
