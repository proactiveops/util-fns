"""Test isoformat_to_timestamp module."""

__author__ = "Dave Hall <me@davehall.com.au>"
__copyright__ = "Copyright 2024, 2025, Skwashd Services Pty Ltd https://davehall.com.au"
__license__ = "MIT"

import datetime

import isoformat_to_timestamp
import pytest


def test_handler(lambda_context: isoformat_to_timestamp.LambdaContext) -> None:
    """Test lambda handler."""
    start = int(datetime.datetime.now(tz=datetime.UTC).timestamp())
    response = isoformat_to_timestamp.handler({}, lambda_context)
    end = int(datetime.datetime.now(tz=datetime.UTC).timestamp()) + 1

    assert response["timestamp"] >= start
    assert response["timestamp"] <= end


def test_handler_with_timestamp(
    lambda_context: isoformat_to_timestamp.LambdaContext,
) -> None:
    """Test lambda handler with timestamp."""
    isoformat = datetime.datetime.now(tz=datetime.UTC)

    event = {"isoformat": isoformat.isoformat()}
    response = isoformat_to_timestamp.handler(event, lambda_context)

    assert response["timestamp"] == int(isoformat.timestamp())


def test_handler_with_invalid_timestamp(
    lambda_context: isoformat_to_timestamp.LambdaContext,
) -> None:
    """Test lambda handler with invalid timestamp."""
    isoformat = "invalid-timestamp"

    event = {"isoformat": isoformat}
    with pytest.raises(ValueError, match="Invalid isoformat string"):
        isoformat_to_timestamp.handler(event, lambda_context)
