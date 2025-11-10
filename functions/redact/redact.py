"""Redact text based on entities identified by Amazon Comprehend."""

__author__ = "Dave Hall <me@davehall.com.au>"
__copyright__ = "Copyright 2024, 2025, Skwashd Services Pty Ltd https://davehall.com.au"
__license__ = "MIT"

from typing import Any

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()


def redact_text(
    text: Any,  # noqa: ANN401 We have to allow garbage input
    entities: list[dict[str, str]],
    ignored_entities: list[str],
) -> str:
    """
    Redact text based on entities identified by Amazon Comprehend.

    Args:
    ----
        text: Text to redact.
        entities: Entities to redact.
        ignored_entities: Entities to ignore.

    Returns:
    -------
        Redacted text.

    """
    if type(text) is not str:
        logger.warning("Received non-string text.")
        return ""

    if text == "":
        return ""

    if not entities:
        return text

    # We work backwards to avoid changing the offsets of the entities
    entities = sorted(entities, key=lambda x: int(x["EndOffset"]), reverse=True)
    for entity in entities:
        if entity["Type"] in ignored_entities:
            continue

        text = "".join([
            text[: int(entity["BeginOffset"])],
            entity["Type"],
            text[int(entity["EndOffset"]) :],
        ])

    return str(text)  # Happy now mypy?!


# We don't log the payload as it may contain sensitive information
@logger.inject_lambda_context()
def handler(event: dict, _: LambdaContext) -> dict[str, str]:
    """
    Redact text based on entities identified by Amazon Comprehend.

    Args:
    ----
        event: Event payload.
        _: LambdaContext: AWS Lambda Context object.

    Returns:
    -------
        JSON response.

    """
    text = event.get("text")
    entities: list[dict[str, str]] = event.get("entities")  # type: ignore[assignment]
    ignored_entities: list[str] = event.get("ignored_entities", [])

    response = {
        "clean_text": redact_text(text, entities, ignored_entities),
    }

    logger.debug("Response", extra=response)

    return response
