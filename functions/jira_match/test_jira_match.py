"""Test cases for the jira_match lambda function."""

__author__ = "Dave Hall <me@davehall.com.au>"
__copyright__ = "Copyright 2024, 2025, Skwashd Services Pty Ltd https://davehall.com.au"
__license__ = "MIT"

import jira_match
import pytest
from aws_lambda_powertools.utilities.typing import LambdaContext


@pytest.mark.parametrize(
    ("payload", "expected"),
    [
        ("ABC-123", ["ABC-123"]),
        ("", []),
        ("abc-123", ["ABC-123"]),
        (
            "The first ticket is TICKET-1 and the second one is XYZ-9999",
            ["TICKET-1", "XYZ-9999"],
        ),
        (
            "[ABC-123] This is a tagged PR summary or something",
            ["ABC-123"],
        ),
        (
            "[ABC-123 ABC-124] This is a tagged PR summary or something",
            ["ABC-123", "ABC-124"],
        ),
        ("Please look at ticket ABC-123.", ["ABC-123"]),
        (
            "Please look at ticket ABC-123\nPlease also look at CBA-321 for me.\nThanks\n\nJane",
            ["ABC-123", "CBA-321"],
        ),
        ("ABC-", []),
    ],
)
def test_find_tickets(payload: str, expected: list[str]) -> None:
    """Test lambda handler with common examples."""
    tickets = jira_match.find_tickets(payload)
    assert tickets == expected


def test_handler(lambda_context: LambdaContext) -> None:
    """Test lambda handler."""
    event = {"string": "ABC-123"}
    response = jira_match.handler(event, lambda_context)
    assert response["tickets"] == ["ABC-123"]


def test_handler_empty_body(lambda_context: LambdaContext) -> None:
    """Test lambda handler with empty payload body."""
    with pytest.raises(ValueError, match="Event body is missing"):
        jira_match.handler({}, lambda_context)
