"""Extract Jira ticket references from a string."""

__author__ = "Dave Hall <me@davehall.com.au>"
__copyright__ = "Copyright 2024, 2025, Skwashd Services Pty Ltd https://davehall.com.au"
__license__ = "MIT"

import re

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()


def find_tickets(body: str) -> list[str]:
    """Find Jira ticket references in a string."""
    # Add a space before and after the ticket number to make the regex simpler.
    s = f" {body.upper()} "
    return re.findall(r"[\s\[]?([A-Z][A-Z_0-9]{0,9}\-[0-9]{1,19})[\.,\?\]]?\s", s)


@logger.inject_lambda_context(log_event=True)
def handler(event: dict[str, str], _: LambdaContext) -> dict[str, list[str]]:
    """Check body property for Jira ticket references."""
    if "string" not in event:
        raise ValueError("Event body is missing")  # noqa: TRY003 We don't need a custom exception class for this

    matches = find_tickets(event["string"])

    response = {"tickets": matches}

    logger.debug("Response", extra=response)

    return response
