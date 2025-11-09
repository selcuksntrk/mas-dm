"""
Health API Tests

Tests for the health check and status endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient


@pytest.mark.unit
def test_root_endpoint(test_client: TestClient):
    """
    Test the root endpoint returns correct response.
    
    Args:
        test_client: FastAPI test client fixture
    """
    response = test_client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "message" in data
    assert "version" in data
    assert data["message"] == "Multi-Agent Decision Making API"


@pytest.mark.unit
def test_health_endpoint(test_client: TestClient):
    """
    Test the health check endpoint returns healthy status.
    
    Args:
        test_client: FastAPI test client fixture
    """
    response = test_client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "status" in data
    assert "version" in data
    assert data["status"] == "healthy"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_root_endpoint_async(async_client: AsyncClient):
    """
    Test the root endpoint with async client.
    
    Args:
        async_client: Async HTTP client fixture
    """
    response = await async_client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "message" in data
    assert "version" in data
    assert data["message"] == "Multi-Agent Decision Making API"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_health_endpoint_async(async_client: AsyncClient):
    """
    Test the health check endpoint with async client.
    
    Args:
        async_client: Async HTTP client fixture
    """
    response = await async_client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "status" in data
    assert data["status"] == "healthy"


@pytest.mark.unit
def test_docs_endpoint(test_client: TestClient):
    """
    Test that API documentation is accessible.
    
    Args:
        test_client: FastAPI test client fixture
    """
    response = test_client.get("/docs")
    
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


@pytest.mark.unit
def test_openapi_endpoint(test_client: TestClient):
    """
    Test that OpenAPI schema is accessible.
    
    Args:
        test_client: FastAPI test client fixture
    """
    response = test_client.get("/openapi.json")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "openapi" in data
    assert "info" in data
    assert "paths" in data
    assert data["info"]["title"] == "Multi-Agent Decision Making API"
