"""Test lookup_key function."""

__author__ = "Dave Hall <me@davehall.com.au>"
__copyright__ = "Copyright 2024, 2025, Skwashd Services Pty Ltd https://davehall.com.au"
__license__ = "MIT"

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
