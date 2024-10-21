"""Test in_list lambda function."""

import in_list
import pytest
from aws_lambda_powertools.utilities.typing import LambdaContext


@pytest.mark.parametrize(
    ("values", "item", "expected"),
    [
        (["apple", "banana", "cherry"], "banana", 1),
        (["apple", "banana", "cherry"], "dragonfruit", -1),
    ],
)
def test_handler(
    lambda_context: LambdaContext, values: list, item: str, expected: int
) -> None:
    """Test in_list lambda function handler."""
    event = {
        "list": values,
        "item": item,
    }

    response = in_list.handler(event, lambda_context)
    assert response["index"] == expected


def test_handler_invalid_type(lambda_context: LambdaContext) -> None:
    """Test in_list lambda function handler with missing key."""
    event = {
        "list": {},
        "item": "text",
    }

    with pytest.raises(TypeError, match="Expected list"):
        in_list.handler(event, lambda_context)


def test_handler_empty_list(lambda_context: LambdaContext) -> None:
    """Test in_list lambda function handler with empty list."""
    event = {
        "list": [],
        "item": "text",
    }

    with pytest.raises(ValueError, match="Received empty list"):
        in_list.handler(event, lambda_context)


def test_handler_missing_key(lambda_context: LambdaContext) -> None:
    """Test in_list lambda function handler with missing key."""
    event = {
        "list": ["apple", "banana", "cherry"],
    }

    with pytest.raises(ValueError, match="Key is missing from event body"):
        in_list.handler(event, lambda_context)
