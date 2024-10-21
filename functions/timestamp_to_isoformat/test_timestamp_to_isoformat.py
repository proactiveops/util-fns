"""Test timestamp_to_isoformat module."""

import datetime

import pytest
import timestamp_to_isoformat
from aws_lambda_powertools.utilities.typing import LambdaContext


def test_handler(lambda_context: LambdaContext) -> None:
    """Test lambda handler."""
    start = int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp())
    response = timestamp_to_isoformat.handler({}, lambda_context)
    end = int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp()) + 1

    as_timestamp = datetime.datetime.fromisoformat(response["isoformat"]).timestamp()

    assert as_timestamp >= start
    assert as_timestamp <= end


def test_handler_with_timestamp(
    lambda_context: LambdaContext,
) -> None:
    """Test lambda handler with timestamp."""
    event = {"timestamp": 1415880000}
    response = timestamp_to_isoformat.handler(event, lambda_context)

    assert response["isoformat"] == "2014-11-13T12:00:00+00:00"


def test_timestamp_to_isoformat_timestamp() -> None:
    """Test timestamp_to_isoformat with invalid timestamp."""
    timestamp = "invalid-timestamp"

    with pytest.raises(
        ValueError, match="could not convert string to float: 'invalid-timestamp'"
    ):
        timestamp_to_isoformat.timestamp_to_isoformat(timestamp)


def test_timestamp_to_isoformat_string() -> None:
    """Test timestamp_to_isoformat with string representation."""
    timestamp = "1415880000"
    isoformat = timestamp_to_isoformat.timestamp_to_isoformat(timestamp)

    assert str(isoformat) == "2014-11-13T12:00:00+00:00"
