"""Global test configuration and fixtures."""

__author__ = "Dave Hall <me@davehall.com.au>"
__copyright__ = "Copyright 2024, 2025, Skwashd Services Pty Ltd https://davehall.com.au"
__license__ = "MIT"

import uuid

import pytest
from aws_lambda_powertools.utilities.typing import LambdaContext


class TestLambdaContext:
    """Mock LambdaContext class to use when testing Lambda functions."""

    def __init__(self) -> None:
        """Initialize Lambda Context."""
        self.function_name = "handler"
        self.memory_limit_in_mb = 128
        self.aws_request_id = uuid.uuid4().hex
        self.invoked_function_arn = f"arn:aws:lambda:eu-east-1:012345678910:function:{__name__[5:]}"  # Drop "test_" from the function name


@pytest.fixture
def lambda_context() -> LambdaContext:
    """Mock Lambda Context object."""
    return TestLambdaContext()
