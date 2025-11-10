"""Global test configuration and fixtures."""

__author__ = "Dave Hall <me@davehall.com.au>"
__copyright__ = "Copyright 2024, 2025, Skwashd Services Pty Ltd https://davehall.com.au"
__license__ = "MIT"

import uuid

import pytest
from aws_lambda_powertools.utilities.typing import LambdaContext


@pytest.fixture
def lambda_context() -> LambdaContext:
    """Mock Lambda Context object."""
    mock_context: LambdaContext = LambdaContext()
    mock_context._function_name = "lhandler"
    mock_context._function_version = "$LATEST"
    mock_context._invoked_function_arn = (
        "arn:aws:lambda:us-east-1:123456789012:function:{__name__[5:]}"
    )
    mock_context._memory_limit_in_mb = 128
    mock_context._aws_request_id = uuid.uuid4().hex
    mock_context._log_group_name = "/aws/lambda/{__name__[5:]}"
    mock_context._log_stream_name = "2023/11/06/[LATEST]abcdef123456"

    return mock_context
