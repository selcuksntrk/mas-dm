"""
Process Manager Tests

Tests for the ProcessManager service layer.
"""

import pytest
from datetime import datetime

from app.services.process_manager import ProcessManager
from app.services.redis_repository import InMemoryProcessRepository
from app.models.domain import ProcessInfo


@pytest.mark.unit
@pytest.mark.asyncio
async def test_process_manager_create_process(process_manager: ProcessManager, sample_decision_query: str):
    """
    Test creating a new process through the manager.
    
    Args:
        process_manager: Process manager fixture
        sample_decision_query: Sample query fixture
    """
    process = await process_manager.create_process(sample_decision_query)
    
    assert process is not None
    assert process.process_id is not None
    assert process.query == sample_decision_query
    assert process.status == "pending"
    assert isinstance(process.created_at, str)  # Stored as ISO format string
    assert process.created_at is not None


@pytest.mark.unit
@pytest.mark.asyncio
async def test_process_manager_get_process(process_manager: ProcessManager, sample_decision_query: str):
    """
    Test retrieving a process through the manager.
    
    Args:
        process_manager: Process manager fixture
        sample_decision_query: Sample query fixture
    """
    # Create a process
    created = await process_manager.create_process(sample_decision_query)
    process_id = created.process_id
    
    # Retrieve it
    retrieved = await process_manager.get_process(process_id)
    
    assert retrieved is not None
    assert retrieved.process_id == process_id
    assert retrieved.query == sample_decision_query


@pytest.mark.unit
@pytest.mark.asyncio
async def test_process_manager_list_all(process_manager: ProcessManager, sample_decision_queries: list[str]):
    """
    Test listing all processes through the manager.
    
    Args:
        process_manager: Process manager fixture
        sample_decision_queries: List of sample queries fixture
    """
    # Create multiple processes
    created_ids = []
    for query in sample_decision_queries[:3]:
        process = await process_manager.create_process(query)
        created_ids.append(process.process_id)
    
    # List all
    all_processes = await process_manager.list_all()
    
    assert len(all_processes) >= 3
    
    # Verify our processes are in the list
    process_ids = [p.process_id for p in all_processes]
    for pid in created_ids:
        assert pid in process_ids


@pytest.mark.unit
@pytest.mark.asyncio
async def test_process_manager_get_stats(process_manager: ProcessManager, sample_decision_query: str):
    """
    Test getting statistics through the manager.
    
    Args:
        process_manager: Process manager fixture
        sample_decision_query: Sample query fixture
    """
    # Create some processes
    await process_manager.create_process(sample_decision_query)
    
    # Get stats
    stats = await process_manager.get_stats()
    
    assert "total" in stats
    assert stats["total"] >= 1
    assert "pending" in stats


@pytest.mark.unit
@pytest.mark.asyncio
async def test_process_manager_cleanup(process_manager: ProcessManager):
    """
    Test cleanup through the manager.
    
    Args:
        process_manager: Process manager fixture
    """
    # Create a completed process directly in repository
    repository = process_manager._repository
    
    completed_process = ProcessInfo(
        process_id="cleanup-manager-test",
        query="Cleanup test",
        status="completed",
        created_at=datetime.now(),
    )
    
    await repository.save(completed_process)
    
    # Cleanup
    removed_count = await process_manager.cleanup_completed()
    
    assert removed_count >= 1


@pytest.mark.unit
@pytest.mark.asyncio
async def test_process_manager_exists(process_manager: ProcessManager, sample_decision_query: str):
    """
    Test checking process existence through the manager.
    
    Args:
        process_manager: Process manager fixture
        sample_decision_query: Sample query fixture
    """
    # Create a process
    process = await process_manager.create_process(sample_decision_query)
    
    # Check existence
    exists = await process_manager.exists(process.process_id)
    assert exists is True
    
    # Check non-existent
    exists_false = await process_manager.exists("does-not-exist")
    assert exists_false is False


@pytest.mark.unit
@pytest.mark.asyncio
async def test_process_manager_unique_ids(process_manager: ProcessManager, sample_decision_query: str):
    """
    Test that process IDs are unique.
    
    Args:
        process_manager: Process manager fixture
        sample_decision_query: Sample query fixture
    """
    # Create multiple processes
    process_ids = []
    for _ in range(10):
        process = await process_manager.create_process(sample_decision_query)
        process_ids.append(process.process_id)
    
    # Verify all IDs are unique
    assert len(set(process_ids)) == len(process_ids)


@pytest.mark.unit
@pytest.mark.asyncio
async def test_process_manager_update_process(process_manager: ProcessManager, sample_decision_query: str):
    """
    Test updating a process through the manager.
    
    Args:
        process_manager: Process manager fixture
        sample_decision_query: Sample query fixture
    """
    # Create a process
    process = await process_manager.create_process(sample_decision_query)
    original_id = process.process_id
    
    # Update status through repository
    process.status = "running"
    await process_manager._repository.save(process)
    
    # Retrieve and verify
    retrieved = await process_manager.get_process(original_id)
    
    assert retrieved is not None
    assert retrieved.status == "running"


@pytest.mark.unit
def test_process_manager_initialization():
    """
    Test that ProcessManager can be initialized with and without repository.
    """
    # With explicit repository
    repo = InMemoryProcessRepository()
    manager = ProcessManager(repository=repo)
    assert manager._repository is repo
    
    # Without repository (should create default)
    manager2 = ProcessManager()
    assert manager2._repository is not None


@pytest.mark.slow
@pytest.mark.integration
@pytest.mark.asyncio
async def test_process_manager_execute_full(process_manager: ProcessManager, sample_decision_query: str):
    """
    Test full process execution through the manager.
    
    WARNING: This test makes real AI API calls and will take several minutes.
    Only run with pytest -m slow flag.
    
    Args:
        process_manager: Process manager fixture
        sample_decision_query: Sample query fixture
    """
    # Create a process
    process = await process_manager.create_process(sample_decision_query)
    process_id = process.process_id
    
    # Execute it
    await process_manager.execute_process(process_id)
    
    # Retrieve completed process
    completed = await process_manager.get_process(process_id)
    
    assert completed is not None
    assert completed.status in ["completed", "failed"]
    
    if completed.status == "completed":
        assert completed.result is not None
        # Result is a DecisionState object, check its attributes
        assert hasattr(completed.result, "result")
        assert hasattr(completed.result, "result_comment")
        assert completed.result.result  # Check it has content
