"""Test in_string function."""

import in_string
import pytest
from aws_lambda_powertools.utilities.typing import LambdaContext


@pytest.mark.parametrize(
    ("string", "substring", "expected"),
    [
        ("pneumonoultramicroscopicsilicovolcanoconiosis", "microscopic", 13),
        ("team", "i", -1),
    ],
)
def test_handler(
    lambda_context: LambdaContext, string: list, substring: str, expected: int
) -> None:
    """Test in_string lambda function handler."""
    event = {
        "string": string,
        "substring": substring,
    }

    response = in_string.handler(event, lambda_context)
    assert response["index"] == expected


def test_handler_invalid_type(lambda_context: LambdaContext) -> None:
    """Test in_string lambda function handler with invalid type."""
    event = {
        "string": {},
        "substring": "text",
    }

    with pytest.raises(TypeError, match="Expected string"):
        in_string.handler(event, lambda_context)


def test_handler_missing_string(lambda_context: LambdaContext) -> None:
    """Test in_string lambda function handler missing string."""
    event = {
        "substring": "text",
    }

    with pytest.raises(TypeError, match="Expected string"):
        in_string.handler(event, lambda_context)


def test_handler_empty_string(lambda_context: LambdaContext) -> None:
    """Test in_string lambda function handler with empty string."""
    event = {
        "string": "",
        "substring": "text",
    }

    with pytest.raises(ValueError, match="Received empty string"):
        in_string.handler(event, lambda_context)


def test_handler_missing_substring(lambda_context: LambdaContext) -> None:
    """Test in_string lambda function handler missing substring."""
    event = {
        "string": "text",
    }

    with pytest.raises(TypeError, match="Expected string"):
        in_string.handler(event, lambda_context)


def test_handler_empty_substring(lambda_context: LambdaContext) -> None:
    """Test in_string lambda function handler with empty substring."""
    event = {
        "string": "text",
        "substring": "",
    }

    with pytest.raises(ValueError, match="Received empty substring"):
        in_string.handler(event, lambda_context)
