"""Test cases for ip_to_object function."""

__author__ = "Dave Hall <me@davehall.com.au>"
__copyright__ = "Copyright 2024, 2025, Skwashd Services Pty Ltd https://davehall.com.au"
__license__ = "MIT"

import ip_to_object
import pytest
from aws_lambda_powertools.utilities.typing import LambdaContext


@pytest.mark.parametrize(
    ("ip", "as_int", "version"),
    [
        ("203.0.113.1", 3405803777, 4),
        ("2001:db8::1", 42540766411282592856903984951653826561, 6),
    ],
)
def test_ip_to_object(ip: str, as_int: int, version: int) -> None:
    """Test ip_to_object function."""
    ip_info = ip_to_object.IPInfo(ip)
    assert ip_info.to_dict()["int"] == as_int
    assert ip_info.to_dict()["version"] == version


def test_ip_to_object_str() -> None:
    """Test ip_to_object function string representation."""
    ip = "1.2.3.4"
    ip_info = ip_to_object.IPInfo(ip)
    assert str(ip_info) == ip


def test_ip_to_object_int() -> None:
    """Test ip_to_object function string representation."""
    ip_info = ip_to_object.IPInfo("203.0.113.1")
    assert int(ip_info) == 3405803777


def test_handler_invalid_ip(lambda_context: LambdaContext) -> None:
    """Test ip_to_object function with invalid IP."""
    with pytest.raises(ip_to_object.InvalidIPError):
        ip_to_object.handler({"ip": "123"}, lambda_context)


def test_handler_missing_ip(lambda_context: LambdaContext) -> None:
    """Test ip_to_object function with invalid IP."""
    with pytest.raises(ValueError, match="IP address missing from event body"):
        ip_to_object.handler({}, lambda_context)


def test_handler(lambda_context: LambdaContext) -> None:
    """Test ip_to_object function."""
    event = {"ip": "203.0.113.1"}
    response = ip_to_object.handler(event, lambda_context)
    assert response["int"] == 3405803777
    assert response["version"] == 4
