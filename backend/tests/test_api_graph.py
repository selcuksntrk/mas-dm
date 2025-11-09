"""
Graph API Tests

Tests for the graph visualization endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient


@pytest.mark.unit
def test_graph_mermaid_endpoint(test_client: TestClient):
    """
    Test the mermaid diagram endpoint returns valid diagram code.
    
    Args:
        test_client: FastAPI test client fixture
    """
    response = test_client.get("/graph/mermaid")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "mermaid_code" in data
    assert isinstance(data["mermaid_code"], str)
    assert len(data["mermaid_code"]) > 0
    
    # Check that it contains mermaid graph syntax
    mermaid_code = data["mermaid_code"]
    assert "graph" in mermaid_code.lower()
    

@pytest.mark.unit
def test_graph_structure_endpoint(test_client: TestClient):
    """
    Test the graph structure endpoint returns correct metadata.
    
    Args:
        test_client: FastAPI test client fixture
    """
    response = test_client.get("/graph/structure")
    
    assert response.status_code == 200
    data = response.json()
    
    # Check structure metadata
    assert "total_nodes" in data
    assert "agent_nodes" in data
    assert "evaluator_nodes" in data
    
    # Validate counts
    assert isinstance(data["total_nodes"], int)
    assert isinstance(data["agent_nodes"], int)
    assert isinstance(data["evaluator_nodes"], int)
    assert data["total_nodes"] > 0
    assert data["agent_nodes"] > 0
    assert data["evaluator_nodes"] >= 0
    
    # Check nodes list
    assert "nodes" in data
    assert isinstance(data["nodes"], list)
    assert len(data["nodes"]) == data["total_nodes"]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_graph_mermaid_async(async_client: AsyncClient):
    """
    Test the mermaid endpoint with async client.
    
    Args:
        async_client: Async HTTP client fixture
    """
    response = await async_client.get("/graph/mermaid")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "mermaid_code" in data
    assert len(data["mermaid_code"]) > 100  # Should be substantial


@pytest.mark.unit
@pytest.mark.asyncio
async def test_graph_structure_async(async_client: AsyncClient):
    """
    Test the graph structure endpoint with async client.
    
    Args:
        async_client: Async HTTP client fixture
    """
    response = await async_client.get("/graph/structure")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "total_nodes" in data
    assert "nodes" in data
    assert isinstance(data["nodes"], list)


@pytest.mark.unit
def test_graph_mermaid_contains_key_nodes(test_client: TestClient):
    """
    Test that mermaid diagram contains expected node names.
    
    Args:
        test_client: FastAPI test client fixture
    """
    response = test_client.get("/graph/mermaid")
    
    assert response.status_code == 200
    data = response.json()
    mermaid_code = data["mermaid_code"].lower()
    
    # Check for key nodes that should exist in the graph
    expected_nodes = [
        "trigger",
        "root",
        "scope",
        "draft",
        "alternative",
    ]
    
    for node in expected_nodes:
        assert node in mermaid_code, f"Expected node '{node}' not found in mermaid diagram"


@pytest.mark.unit
def test_graph_structure_nodes_have_names(test_client: TestClient):
    """
    Test that all nodes in structure have name attribute.
    
    Args:
        test_client: FastAPI test client fixture
    """
    response = test_client.get("/graph/structure")
    
    assert response.status_code == 200
    data = response.json()
    
    nodes = data["nodes"]
    assert len(nodes) > 0
    
    for node in nodes:
        assert "name" in node or "id" in node, "Node should have name or id"
