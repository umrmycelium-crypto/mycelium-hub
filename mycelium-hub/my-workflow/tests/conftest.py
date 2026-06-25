"""Pytest configuration and fixtures for Mistral Workflows testing.

This module provides:
- Common fixtures for workflow testing
- Mock configurations for Mistral AI client
- Test utilities for activities and workflows
"""

import asyncio
import json
import os
from pathlib import Path
from typing import Any, AsyncGenerator, Generator
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest
from pydantic import BaseModel

# Mock environment variables for testing
@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set up mock environment variables for all tests."""
    monkeypatch.setenv("MISTRAL_API_KEY", "test_api_key")
    monkeypatch.setenv("SERVER_URL", "https://api.test.mistral.ai")
    monkeypatch.setenv("DEPLOYMENT_NAME", "test-deployment")


@pytest.fixture
def project_root() -> Path:
    """Return the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def src_root() -> Path:
    """Return the src directory."""
    return Path(__file__).parent.parent / "src"


# =============================================================================
# Mistral Workflows Fixtures
# =============================================================================

@pytest.fixture
def mock_mistral_client() -> MagicMock:
    """Create a mock Mistral workflows client."""
    client = MagicMock()
    client.workflows = MagicMock()
    client.workflows.execute_workflow_and_wait_async = AsyncMock()
    return client


@pytest.fixture
def mock_workflow_context() -> MagicMock:
    """Create a mock workflow execution context."""
    context = MagicMock()
    context.workflow_id = "test-workflow-id"
    context.run_id = "test-run-id"
    return context


# =============================================================================
# Async Fixtures
# =============================================================================

@pytest.fixture
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


# =============================================================================
# Test Data Fixtures
# =============================================================================

@pytest.fixture
def sample_claim_input() -> dict[str, Any]:
    """Sample input for insurance claims workflow."""
    return {
        "claim_id": "CLM-001",
        "claimant_name": "Jane Smith",
        "description": "My car was hit from behind at a stop light",
        "photos": [
            "file:///path/to/photo1.jpg",
            "file:///path/to/photo2.jpg",
        ],
    }


@pytest.fixture
def sample_cargo_input() -> dict[str, Any]:
    """Sample input for cargo release workflow."""
    return {
        "document_uri": "file:///path/to/shipping_doc.pdf",
        "shipment_id": "BL-2024-HAM-009371",
    }


@pytest.fixture
def sample_linear_input() -> dict[str, Any]:
    """Sample input for linear summarization workflow."""
    return {
        "team": "Engineering",
        "project": "Roadmap",
    }


@pytest.fixture
def sample_modernization_input() -> dict[str, Any]:
    """Sample input for code modernization workflow."""
    return {
        "repo_path": "src/examples/code_modernization/sample_data/legacy_repo",
        "target": "Python 2.7 → 3.12",
    }


# =============================================================================
# Mock Activity Fixtures
# =============================================================================

@pytest.fixture
def mock_activity():
    """Create a mock workflows activity."""
    activity = MagicMock()
    activity.__name__ = "mock_activity"
    return activity


@pytest.fixture
def mock_workflow_class():
    """Create a mock workflow class."""
    workflow_class = MagicMock()
    workflow_class.__workflows_workflow_def__ = MagicMock()
    return workflow_class


# =============================================================================
# Pydantic Model Test Utilities
# =============================================================================

class TestPydanticModel(BaseModel):
    """Base class for testing Pydantic models."""
    
    @classmethod
    def test_validation(cls, test_data: dict[str, Any]) -> None:
        """Test that a model validates correctly."""
        instance = cls.model_validate(test_data)
        assert instance is not None
        
    @classmethod
    def test_serialization(cls, test_data: dict[str, Any]) -> None:
        """Test that a model serializes correctly."""
        instance = cls.model_validate(test_data)
        json_data = instance.model_dump_json()
        assert json.loads(json_data) == test_data


# =============================================================================
# File System Fixtures
# =============================================================================

@pytest.fixture
def temp_test_file(tmp_path: Path) -> Path:
    """Create a temporary test file."""
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("test content")
    return test_file


@pytest.fixture
def temp_json_file(tmp_path: Path) -> Path:
    """Create a temporary JSON test file."""
    test_file = tmp_path / "test_data.json"
    test_file.write_text(json.dumps({"key": "value"}, indent=2))
    return test_file


# =============================================================================
# Mock Connector Fixtures
# =============================================================================

@pytest.fixture
def mock_connector():
    """Create a mock MCP connector."""
    connector = MagicMock()
    connector.call_tool = AsyncMock()
    return connector


@pytest.fixture
def mock_linear_connector():
    """Create a mock Linear connector with typical responses."""
    connector = MagicMock()
    
    async def mock_call_tool(tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if tool_name == "list_teams":
            return {
                "content": [{
                    "type": "text",
                    "text": json.dumps({
                        "teams": [
                            {"id": "team-1", "name": "Engineering"},
                            {"id": "team-2", "name": "Product"},
                        ]
                    })
                }]
            }
        elif tool_name == "list_issues":
            return {
                "content": [{
                    "type": "text",
                    "text": json.dumps({
                        "issues": [
                            {"id": "issue-1", "title": "Test Issue", "state": {"name": "Todo"}}
                        ]
                    })
                }]
            }
        return {"content": []}
    
    connector.call_tool = mock_call_tool
    return connector
