"""Lambda function to find a value in a list."""

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()


@logger.inject_lambda_context(log_event=True)
def handler(event: dict[str, any], _: LambdaContext) -> dict[str, str]:
    """
    Find a value in a list.

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
    values = event.get("list")
    # JSON converts empty objects to empty lists, so we need to check for this.
    if type(values) is not list:
        logger.info("Recevied invalid list.")
        raise TypeError(f"Expected list, received {type(values)} for list")  # noqa: TRY003 We don't need a custom exception class for this

    if len(values) == 0:
        logger.info("Recevied empty list.")
        raise ValueError("Received empty list")  # noqa: TRY003 We don't need a custom exception class for this

    key = event.get("item")
    if not key:
        logger.error("Key is missing from event body")
        raise ValueError("Key is missing from event body")  # noqa: TRY003 We don't need a custom exception class for this

    try:
        index = values.index(key)
    except ValueError:
        index = -1

    response = {"index": index}

    logger.debug("Response", extra=response)

    return response
