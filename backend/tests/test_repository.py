"""
Repository Tests

Tests for the repository layer (InMemoryProcessRepository and RedisProcessRepository).
"""

import pytest
from datetime import datetime

from app.services.redis_repository import InMemoryProcessRepository
from app.models.domain import ProcessInfo


def _get_now_iso() -> str:
    """Helper to get current time as ISO string."""
    return datetime.now().isoformat()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_repository_save_and_get(in_memory_repository: InMemoryProcessRepository):
    """
    Test saving and retrieving a process.
    
    Args:
        in_memory_repository: In-memory repository fixture
    """
    # Create a test process
    process = ProcessInfo(
        process_id="test-123",
        query="Should I test this?",
        status="pending",
        created_at=_get_now_iso(),
    )
    
    # Save it
    await in_memory_repository.save(process)
    
    # Retrieve it
    retrieved = await in_memory_repository.get("test-123")
    
    assert retrieved is not None
    assert retrieved.process_id == "test-123"
    assert retrieved.query == "Should I test this?"
    assert retrieved.status == "pending"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_repository_exists(in_memory_repository: InMemoryProcessRepository):
    """
    Test checking if a process exists.
    
    Args:
        in_memory_repository: In-memory repository fixture
    """
    # Create and save a process
    process = ProcessInfo(
        process_id="exists-test",
        
        status="running",
        created_at=_get_now_iso(),
    )
    
    await in_memory_repository.save(process)
    
    # Check existence
    assert await in_memory_repository.exists("exists-test") is True
    assert await in_memory_repository.exists("nonexistent") is False


@pytest.mark.unit
@pytest.mark.asyncio
async def test_repository_delete(in_memory_repository: InMemoryProcessRepository):
    """
    Test deleting a process.
    
    Args:
        in_memory_repository: In-memory repository fixture
    """
    # Create and save a process
    process = ProcessInfo(
        process_id="delete-test",
        
        status="completed",
        created_at=_get_now_iso(),
    )
    
    await in_memory_repository.save(process)
    assert await in_memory_repository.exists("delete-test") is True
    
    # Delete it
    deleted = await in_memory_repository.delete("delete-test")
    
    assert deleted is True
    assert await in_memory_repository.exists("delete-test") is False


@pytest.mark.unit
@pytest.mark.asyncio
async def test_repository_list_all(in_memory_repository: InMemoryProcessRepository):
    """
    Test listing all processes.
    
    Args:
        in_memory_repository: In-memory repository fixture
    """
    # Create multiple processes
    processes = [
        ProcessInfo(
            process_id=f"list-test-{i}",
            
            status="pending",
            created_at=_get_now_iso(),
        )
        for i in range(5)
    ]
    
    # Save all
    for process in processes:
        await in_memory_repository.save(process)
    
    # List all
    all_processes = await in_memory_repository.list_all()
    
    assert len(all_processes) >= 5
    
    # Verify our processes are in the list
    process_ids = [p.process_id for p in all_processes]
    for i in range(5):
        assert f"list-test-{i}" in process_ids


@pytest.mark.unit
@pytest.mark.asyncio
async def test_repository_get_stats(in_memory_repository: InMemoryProcessRepository):
    """
    Test getting repository statistics.
    
    Args:
        in_memory_repository: In-memory repository fixture
    """
    # Create processes with different statuses
    statuses = ["pending", "running", "completed", "failed"]
    
    for i, status in enumerate(statuses):
        process = ProcessInfo(
            process_id=f"stats-test-{i}",
            
            status=status,
            created_at=_get_now_iso(),
        )
        await in_memory_repository.save(process)
    
    # Get stats
    stats = await in_memory_repository.get_stats()
    
    assert "total" in stats
    assert stats["total"] >= 4
    
    # Check status counts
    for status in statuses:
        assert status in stats
        assert stats[status] >= 1


@pytest.mark.unit
@pytest.mark.asyncio
async def test_repository_cleanup_completed(in_memory_repository: InMemoryProcessRepository):
    """
    Test cleaning up completed processes.
    
    Args:
        in_memory_repository: In-memory repository fixture
    """
    # Create completed and non-completed processes
    completed_process = ProcessInfo(
        process_id="cleanup-completed",
        
        status="completed",
        created_at=_get_now_iso(),
    )
    
    pending_process = ProcessInfo(
        process_id="cleanup-pending",
        
        status="pending",
        created_at=_get_now_iso(),
    )
    
    await in_memory_repository.save(completed_process)
    await in_memory_repository.save(pending_process)
    
    # Cleanup
    removed_count = await in_memory_repository.cleanup_completed()
    
    assert removed_count >= 1
    
    # Verify completed is gone but pending remains
    assert await in_memory_repository.exists("cleanup-completed") is False
    assert await in_memory_repository.exists("cleanup-pending") is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_repository_update_status(in_memory_repository: InMemoryProcessRepository):
    """
    Test updating a process status.
    
    Args:
        in_memory_repository: In-memory repository fixture
    """
    # Create a process
    process = ProcessInfo(
        process_id="update-test",
        
        status="pending",
        created_at=_get_now_iso(),
    )
    
    await in_memory_repository.save(process)
    
    # Update status
    process.status = "running"
    await in_memory_repository.save(process)
    
    # Retrieve and verify
    retrieved = await in_memory_repository.get("update-test")
    
    assert retrieved is not None
    assert retrieved.status == "running"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_repository_get_nonexistent(in_memory_repository: InMemoryProcessRepository):
    """
    Test retrieving a nonexistent process returns None.
    
    Args:
        in_memory_repository: In-memory repository fixture
    """
    retrieved = await in_memory_repository.get("does-not-exist")
    
    assert retrieved is None


@pytest.mark.unit
@pytest.mark.asyncio
async def test_repository_delete_nonexistent(in_memory_repository: InMemoryProcessRepository):
    """
    Test deleting a nonexistent process returns False.
    
    Args:
        in_memory_repository: In-memory repository fixture
    """
    deleted = await in_memory_repository.delete("does-not-exist")
    
    assert deleted is False


@pytest.mark.unit
@pytest.mark.asyncio
async def test_repository_with_result(in_memory_repository: InMemoryProcessRepository):
    """
    Test saving and retrieving a process with result.
    
    Args:
        in_memory_repository: In-memory repository fixture
    """
    # Create a process with result
    process = ProcessInfo(
        process_id="result-test",
        
        status="completed",
        created_at=_get_now_iso(),
        result={
            "selected_decision": "Yes, proceed",
            "alternative_decision": "No, wait",
        }
    )
    
    await in_memory_repository.save(process)
    
    # Retrieve and verify
    retrieved = await in_memory_repository.get("result-test")
    
    assert retrieved is not None
    assert retrieved.result is not None
    assert retrieved.result["selected_decision"] == "Yes, proceed"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_repository_with_error(in_memory_repository: InMemoryProcessRepository):
    """
    Test saving and retrieving a process with error.
    
    Args:
        in_memory_repository: In-memory repository fixture
    """
    # Create a failed process
    process = ProcessInfo(
        process_id="error-test",
        
        status="failed",
        created_at=_get_now_iso(),
        error="Something went wrong"
    )
    
    await in_memory_repository.save(process)
    
    # Retrieve and verify
    retrieved = await in_memory_repository.get("error-test")
    
    assert retrieved is not None
    assert retrieved.status == "failed"
    assert retrieved.error == "Something went wrong"
