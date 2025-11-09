"""
Decision API Tests

Tests for the decision-making endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient


@pytest.mark.unit
def test_list_processes_empty(test_client: TestClient):
    """
    Test listing processes when none exist.
    
    Args:
        test_client: FastAPI test client fixture
    """
    response = test_client.get("/decisions/processes")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "processes" in data
    assert "stats" in data
    assert isinstance(data["processes"], list)


@pytest.mark.unit
@pytest.mark.asyncio
async def test_start_decision_async(async_client: AsyncClient, sample_decision_query: str):
    """
    Test starting an async decision process.
    
    Note: This test does not wait for completion, just verifies the process starts.
    
    Args:
        async_client: Async HTTP client fixture
        sample_decision_query: Sample query fixture
    """
    response = await async_client.post(
        "/decisions/start",
        json={"decision_query": sample_decision_query}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "process_id" in data
    assert "status" in data
    assert "message" in data
    assert data["status"] in ["pending", "running"]
    
    # Verify the process_id is a valid string
    process_id = data["process_id"]
    assert isinstance(process_id, str)
    assert len(process_id) > 0


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_process_status(async_client: AsyncClient, sample_decision_query: str):
    """
    Test getting status of a decision process.
    
    Args:
        async_client: Async HTTP client fixture
        sample_decision_query: Sample query fixture
    """
    # First, start a process
    start_response = await async_client.post(
        "/decisions/start",
        json={"decision_query": sample_decision_query}
    )
    
    assert start_response.status_code == 200
    process_id = start_response.json()["process_id"]
    
    # Now check its status
    status_response = await async_client.get(f"/decisions/status/{process_id}")
    
    assert status_response.status_code == 200
    data = status_response.json()
    
    assert "process_id" in data
    assert "status" in data
    assert data["process_id"] == process_id
    assert data["status"] in ["pending", "running", "completed", "failed"]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_nonexistent_process(async_client: AsyncClient):
    """
    Test getting status of a process that doesn't exist.
    
    Args:
        async_client: Async HTTP client fixture
    """
    response = await async_client.get("/decisions/status/nonexistent-id-12345")
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data


@pytest.mark.unit
@pytest.mark.asyncio
async def test_list_processes_after_creation(async_client: AsyncClient, sample_decision_query: str):
    """
    Test listing processes after creating one.
    
    Args:
        async_client: Async HTTP client fixture
        sample_decision_query: Sample query fixture
    """
    # Create a process
    start_response = await async_client.post(
        "/decisions/start",
        json={"decision_query": sample_decision_query}
    )
    
    assert start_response.status_code == 200
    
    # List processes
    list_response = await async_client.get("/decisions/processes")
    
    assert list_response.status_code == 200
    data = list_response.json()
    
    assert "processes" in data
    assert "stats" in data
    assert len(data["processes"]) >= 1
    
    # Check stats
    stats = data["stats"]
    assert "total" in stats
    assert stats["total"] >= 1


@pytest.mark.unit
@pytest.mark.asyncio
async def test_cleanup_processes(async_client: AsyncClient):
    """
    Test cleaning up completed processes.
    
    Args:
        async_client: Async HTTP client fixture
    """
    response = await async_client.delete("/decisions/cleanup")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "message" in data
    assert "removed_count" in data or "deleted_count" in data
    assert "remaining_processes" in data
    assert "stats" in data


@pytest.mark.unit
def test_invalid_decision_query_empty(test_client: TestClient):
    """
    Test that empty decision query is rejected.
    
    Args:
        test_client: FastAPI test client fixture
    """
    response = test_client.post(
        "/decisions/start",
        json={"decision_query": ""}
    )
    
    # Should fail validation
    assert response.status_code == 422


@pytest.mark.unit
def test_invalid_decision_query_missing(test_client: TestClient):
    """
    Test that missing decision query is rejected.
    
    Args:
        test_client: FastAPI test client fixture
    """
    response = test_client.post(
        "/decisions/start",
        json={}
    )
    
    # Should fail validation
    assert response.status_code == 422


@pytest.mark.unit
@pytest.mark.asyncio
async def test_multiple_processes(async_client: AsyncClient, sample_decision_queries: list[str]):
    """
    Test creating multiple decision processes.
    
    Args:
        async_client: Async HTTP client fixture
        sample_decision_queries: List of sample queries fixture
    """
    process_ids = []
    
    # Create multiple processes
    for query in sample_decision_queries[:3]:  # Test with first 3 queries
        response = await async_client.post(
            "/decisions/start",
            json={"decision_query": query}
        )
        
        assert response.status_code == 200
        data = response.json()
        process_ids.append(data["process_id"])
    
    # Verify all processes are unique
    assert len(set(process_ids)) == len(process_ids)
    
    # List all processes
    list_response = await async_client.get("/decisions/processes")
    
    assert list_response.status_code == 200
    data = list_response.json()
    
    # Should have at least the processes we created
    assert len(data["processes"]) >= len(process_ids)


@pytest.mark.slow
@pytest.mark.integration
@pytest.mark.asyncio
async def test_decision_run_sync_full(async_client: AsyncClient, sample_decision_query: str):
    """
    Test full synchronous decision execution.
    
    WARNING: This test makes real AI API calls and will take several minutes.
    Only run with pytest -m slow flag.
    
    Args:
        async_client: Async HTTP client fixture
        sample_decision_query: Sample query fixture
    """
    response = await async_client.post(
        "/decisions/run",
        json={"decision_query": sample_decision_query},
        timeout=300.0  # 5 minutes
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify all required fields are present
    assert "selected_decision" in data
    assert "selected_decision_comment" in data
    assert "alternative_decision" in data
    assert "alternative_decision_comment" in data
    
    # Verify content is not empty
    assert len(data["selected_decision"]) > 0
    assert len(data["alternative_decision"]) > 0
