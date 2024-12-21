"""Test cases for the redact function."""

from aws_lambda_powertools.utilities.typing import LambdaContext
from redact import handler, redact_text


def test_redact_single_entity() -> None:
    """Test redacting a single entity."""
    text = "Hello John Doe"
    entities = [{"BeginOffset": "6", "EndOffset": "14", "Type": "NAME"}]
    expected = "Hello NAME"
    assert redact_text(text, entities, []) == expected


def test_redact_multiple_entities() -> None:
    """Test redacting multiple entities."""
    text = "John Doe lives in Seattle"
    entities = [
        {"BeginOffset": "0", "EndOffset": "8", "Type": "NAME"},
        {"BeginOffset": "18", "EndOffset": "25", "Type": "ADDRESS"},
    ]
    expected = "NAME lives in ADDRESS"
    assert redact_text(text, entities, []) == expected


def test_redact_overlapping_entities() -> None:
    """Test redacting overlapping entities."""
    text = "John Smith Jones"
    entities = [
        {"BeginOffset": "0", "EndOffset": "10", "Type": "NAME"},
        {"BeginOffset": "5", "EndOffset": "16", "Type": "NAME"},
    ]
    expected = "NAME"
    assert redact_text(text, entities, []) == expected


def test_redact_no_entities() -> None:
    """Test redacting a string with no entities."""
    text = "Hello world"
    entities = []
    expected = "Hello world"
    assert redact_text(text, entities, []) == expected


def test_redact_empty_text() -> None:
    """Test redacting an empty string."""
    text = ""
    entities = [{"BeginOffset": "0", "EndOffset": "0", "Type": "NAME"}]
    expected = ""
    assert redact_text(text, entities, []) == expected


def test_redact_with_ignored_entities() -> None:
    """Test redacting with ignored entity types."""
    text = "John works at Microsoft"
    entities = [
        {"BeginOffset": "0", "EndOffset": "4", "Type": "NAME"},
        {"BeginOffset": "13", "EndOffset": "22", "Type": "ORGANIZATION"},
    ]
    ignored_entities = ["ORGANIZATION"]
    expected = "NAME works at Microsoft"
    assert redact_text(text, entities, ignored_entities) == expected


def test_redact_with_multiple_ignored_entities() -> None:
    """Test redacting with multiple ignored entity types."""
    text = "John lives in Seattle and works at Microsoft"
    entities = [
        {"BeginOffset": "0", "EndOffset": "4", "Type": "NAME"},
        {"BeginOffset": "13", "EndOffset": "20", "Type": "ADDRESS"},
        {"BeginOffset": "31", "EndOffset": "40", "Type": "ORGANIZATION"},
    ]
    ignored_entities = ["ADDRESS", "ORGANIZATION"]
    expected = "NAME lives in Seattle and works at Microsoft"
    assert redact_text(text, entities, ignored_entities) == expected


def test_redact_with_all_ignored_entities() -> None:
    """Test redacting when all entity types are ignored."""
    text = "John lives in Seattle"
    entities = [
        {"BeginOffset": "0", "EndOffset": "4", "Type": "NAME"},
        {"BeginOffset": "13", "EndOffset": "20", "Type": "ADDRESS"},
    ]
    ignored_entities = ["NAME", "ADDRESS"]
    expected = "John lives in Seattle"
    assert redact_text(text, entities, ignored_entities) == expected


def test_handler_with_valid_input(lambda_context: LambdaContext) -> None:
    """Test handler with valid input."""
    event = {
        "text": "John Doe lives in Seattle",
        "entities": [
            {"BeginOffset": "0", "EndOffset": "8", "Type": "NAME"},
            {"BeginOffset": "18", "EndOffset": "25", "Type": "ADDRESS"},
        ],
    }
    expected = {"clean_text": "NAME lives in ADDRESS"}
    assert handler(event, lambda_context) == expected


def test_handler_with_empty_text(lambda_context: LambdaContext) -> None:
    """Test handler with empty text."""
    event = {"text": "", "entities": []}
    expected = {"clean_text": ""}
    assert handler(event, lambda_context) == expected


def test_handler_with_no_entities(lambda_context: LambdaContext) -> None:
    """Test handler with no entities."""
    event = {"text": "Hello world", "entities": []}
    expected = {"clean_text": "Hello world"}
    assert handler(event, lambda_context) == expected


def test_handler_with_missing_text(lambda_context: LambdaContext) -> None:
    """Test handler with missing text field."""
    event = {"entities": []}
    expected = {"clean_text": None}
    assert handler(event, lambda_context) == expected


def test_handler_with_missing_entities(lambda_context: LambdaContext) -> None:
    """Test handler with missing entities field."""
    event = {"text": "Hello world"}
    expected = {"clean_text": "Hello world"}
    assert handler(event, lambda_context) == expected
