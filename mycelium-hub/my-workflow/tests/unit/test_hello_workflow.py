"""Unit tests for the hello workflow.

This module tests:
- Hello workflow execution
- Greet activity function
- Input validation
- Output formatting
"""

import pytest

from src.workflows.hello import HelloInput, HelloWorkflow, greet


# =============================================================================
# Model Tests
# =============================================================================


class TestHelloInput:
    """Tests for HelloInput Pydantic model."""

    def test_default_values(self) -> None:
        """Test that default values work correctly."""
        input_data = HelloInput()
        assert input_data.name == "World"

    def test_custom_values(self) -> None:
        """Test custom input values."""
        input_data = HelloInput(name="Alice")
        assert input_data.name == "Alice"

    def test_validation_with_dict(self) -> None:
        """Test model validation from dictionary."""
        input_data = HelloInput.model_validate({"name": "Bob"})
        assert input_data.name == "Bob"

    def test_serialization(self) -> None:
        """Test model serialization to JSON."""
        input_data = HelloInput(name="Charlie")
        json_str = input_data.model_dump_json()
        assert "Charlie" in json_str


# =============================================================================
# Activity Tests
# =============================================================================


class TestGreetActivity:
    """Tests for the greet activity."""

    @pytest.mark.asyncio
    async def test_greet_with_name(self) -> None:
        """Test greeting with a specific name."""
        result = await greet("Alice")
        assert result == "Hello, Alice! Welcome to Mistral Workflows."

    @pytest.mark.asyncio
    async def test_greet_with_world(self) -> None:
        """Test greeting with 'World'."""
        result = await greet("World")
        assert result == "Hello, World! Welcome to Mistral Workflows."

    @pytest.mark.asyncio
    async def test_greet_with_empty_string(self) -> None:
        """Test greeting with empty string."""
        result = await greet("")
        assert result == "Hello, ! Welcome to Mistral Workflows."

    @pytest.mark.asyncio
    async def test_greet_with_special_characters(self) -> None:
        """Test greeting with special characters in name."""
        result = await greet("José <test>&")
        assert "José <test>&" in result


# =============================================================================
# Workflow Tests
# =============================================================================


class TestHelloWorkflow:
    """Tests for the HelloWorkflow class."""

    @pytest.mark.asyncio
    async def test_workflow_execution(self) -> None:
        """Test that the workflow executes successfully with default input."""
        workflow = HelloWorkflow()
        input_data = HelloInput()
        
        result = await workflow.run(input_data)
        
        # The workflow returns a string directly
        # If running through the SDK, it might be wrapped in a dict with 'result' key
        if isinstance(result, dict):
            assert "result" in result
            assert isinstance(result["result"], str)
            assert "Hello, World!" in result["result"]
        else:
            assert isinstance(result, str)
            assert "Hello, World!" in result

    @pytest.mark.asyncio
    async def test_workflow_with_custom_name(self) -> None:
        """Test workflow execution with custom input."""
        workflow = HelloWorkflow()
        input_data = HelloInput(name="TestUser")
        
        result = await workflow.run(input_data)
        
        if isinstance(result, dict):
            assert "Hello, TestUser!" in result["result"]
        else:
            assert "Hello, TestUser!" in result

    @pytest.mark.asyncio
    async def test_workflow_returns_expected_type(self) -> None:
        """Test that workflow returns expected type (string or dict with result)."""
        workflow = HelloWorkflow()
        input_data = HelloInput(name="Any")
        
        result = await workflow.run(input_data)
        
        # Accept either a direct string or a dict with 'result' key
        assert isinstance(result, (str, dict))
        if isinstance(result, dict):
            assert "result" in result


# =============================================================================
# Edge Case Tests
# =============================================================================


class TestHelloEdgeCases:
    """Edge case tests for hello workflow."""

    @pytest.mark.asyncio
    async def test_long_name(self) -> None:
        """Test with very long name."""
        long_name = "A" * 1000
        result = await greet(long_name)
        assert long_name in result

    @pytest.mark.asyncio
    async def test_unicode_name(self) -> None:
        """Test with unicode characters."""
        unicode_name = "你好世界 🌍"
        result = await greet(unicode_name)
        assert unicode_name in result

    def test_input_model_extra_fields_ignored(self) -> None:
        """Test that extra fields in input are ignored."""
        # Pydantic v2 ignores extra fields by default in model_validate
        input_data = HelloInput.model_validate({"name": "Test", "extra": "field"})
        assert input_data.name == "Test"
        assert not hasattr(input_data, "extra")
