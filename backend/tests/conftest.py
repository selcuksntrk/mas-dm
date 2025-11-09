"""
Pytest Configuration and Fixtures

This module provides shared fixtures and configuration for all tests.
"""

import asyncio
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.services.process_manager import ProcessManager
from app.services.redis_repository import InMemoryProcessRepository


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """
    Create an event loop for the test session.
    
    This fixture ensures that all async tests use the same event loop.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def test_client() -> Generator[TestClient, None, None]:
    """
    Create a test client for synchronous API testing.
    
    This fixture provides a FastAPI TestClient that can be used
    to make synchronous HTTP requests to the API.
    
    Yields:
        TestClient: A configured test client
    """
    with TestClient(app) as client:
        yield client


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """
    Create an async client for asynchronous API testing.
    
    This fixture provides an httpx AsyncClient that can be used
    to make asynchronous HTTP requests to the API.
    
    Yields:
        AsyncClient: A configured async client
    """
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client


@pytest.fixture
def in_memory_repository() -> InMemoryProcessRepository:
    """
    Create an in-memory repository for testing.
    
    This fixture provides a clean InMemoryProcessRepository instance
    for testing without requiring Redis.
    
    Returns:
        InMemoryProcessRepository: A new repository instance
    """
    return InMemoryProcessRepository()


@pytest_asyncio.fixture
async def process_manager(in_memory_repository: InMemoryProcessRepository) -> ProcessManager:
    """
    Create a process manager with in-memory repository.
    
    This fixture provides a ProcessManager configured with an
    in-memory repository for isolated testing.
    
    Args:
        in_memory_repository: The in-memory repository fixture
        
    Returns:
        ProcessManager: A configured process manager
    """
    return ProcessManager(repository=in_memory_repository)


@pytest.fixture
def sample_decision_query() -> str:
    """
    Provide a sample decision query for testing.
    
    Returns:
        str: A sample decision query
    """
    return "Should I invest in renewable energy for my company?"


@pytest.fixture
def sample_decision_queries() -> list[str]:
    """
    Provide multiple sample decision queries for testing.
    
    Returns:
        list[str]: A list of sample decision queries
    """
    return [
        "Should I expand my business to international markets?",
        "Should I hire more software engineers this quarter?",
        "Should I migrate our infrastructure to the cloud?",
        "Should I invest in AI technology for our products?",
        "Should I open a new office location?",
    ]


@pytest.fixture
def mock_decision_result() -> dict:
    """
    Provide a mock decision result for testing.
    
    Returns:
        dict: A mock decision result
    """
    return {
        "selected_decision": "Yes, invest in renewable energy",
        "selected_decision_comment": "Based on analysis of long-term costs and environmental impact",
        "alternative_decision": "Wait 6 months and reassess",
        "alternative_decision_comment": "Allows for market stabilization and better pricing",
        "trigger": "Rising energy costs and corporate sustainability goals",
        "root_cause": "Current energy infrastructure is outdated and inefficient",
        "scope": "Company-wide energy infrastructure upgrade",
        "goals": "Reduce energy costs by 30% and achieve carbon neutrality within 2 years",
    }


# Pytest configuration
def pytest_configure(config):
    """
    Configure pytest with custom markers.
    
    Args:
        config: Pytest configuration object
    """
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "slow: Slow tests that make real API calls")
    config.addinivalue_line("markers", "redis: Tests that require Redis")
