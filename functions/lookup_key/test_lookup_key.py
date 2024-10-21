"""Test lookup_key function."""

import lookup_key
import pytest
from aws_lambda_powertools.utilities.typing import LambdaContext


def test_handler(lambda_context: LambdaContext) -> None:
    """Test lookup_key function."""
    event = {"values": {"key": "value"}, "key": "key"}

    response = lookup_key.handler(event, lambda_context)
    assert response["value"] == "value"


def test_handler_missing_key(lambda_context: LambdaContext) -> None:
    """Test lookup_key function with missing key."""
    event = {
        "values": {
            "key": "value",
        },
    }

    with pytest.raises(ValueError, match="Key is missing from event body"):
        lookup_key.handler(event, lambda_context)


def test_handler_empty_list(lambda_context: LambdaContext) -> None:
    """Test lookup_key function with empty list."""
    event = {
        "values": [],
        "key": "key",
    }

    response = lookup_key.handler(event, lambda_context)

    assert response["value"] is None
