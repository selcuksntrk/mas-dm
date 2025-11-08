# Redis Persistence for Async Processes

## 📚 Overview

This document explains the Redis persistence implementation for async decision-making processes. This is a **critical production feature** that enables process state to survive server restarts and enables horizontal scaling.

---

## 🎯 Why Redis Persistence?

### The Problem We're Solving

**Without persistence:**
```
1. User starts a decision process → returns process_id
2. Server restarts (deploy, crash, etc.)
3. User polls /status/{process_id} → 404 Not Found
4. Process state is lost forever ❌
```

**With Redis persistence:**
```
1. User starts a decision process → stored in Redis
2. Server restarts
3. New server instance connects to same Redis
4. User polls /status/{process_id} → 200 OK with status ✅
5. Process state survives! 🎉
```

### Key Benefits

1. **Durability**: Process state survives server restarts
2. **Scalability**: Multiple server instances share same process storage
3. **Debugging**: Inspect process state even after completion
4. **Monitoring**: Track historical process metrics
5. **Recovery**: Resume failed processes

---

## 🏗️ Architecture: Repository Pattern

### What is the Repository Pattern?

The Repository Pattern is a design pattern that **abstracts data storage away from business logic**.

```
┌─────────────────────────────────────────────┐
│         API Endpoints (FastAPI)             │
│   POST /start, GET /status, DELETE /cleanup │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│         ProcessManager (Business Logic)      │
│   create_process(), get_process(), etc.     │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│      IProcessRepository (Interface)         │
│   Abstract contract: save, get, list, etc.  │
└────────────────┬────────────────────────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
┌──────────────┐  ┌──────────────────┐
│  InMemory    │  │  Redis           │
│  Repository  │  │  Repository      │
│  (dev/test)  │  │  (production)    │
└──────────────┘  └──────────────────┘
```

### Why This Pattern?

#### 1. **Separation of Concerns**

```python
# ProcessManager doesn't know HOW data is stored
class ProcessManager:
    def __init__(self, repository: IProcessRepository):
        self._repository = repository  # Could be Redis, SQL, MongoDB, etc.
    
    async def get_process(self, id: str):
        return await self._repository.get(id)  # Business logic doesn't care!
```

#### 2. **Easy Testing**

```python
# Test with in-memory repository (no Redis needed)
def test_process_manager():
    manager = ProcessManager(repository=InMemoryProcessRepository())
    # Test business logic without external dependencies!
```

#### 3. **Flexible Deployment**

```python
# Development: Use in-memory (fast, no setup)
dev_repo = InMemoryProcessRepository()

# Production: Use Redis (persistent, scalable)
prod_repo = RedisProcessRepository()

# Both work with same ProcessManager code!
```

#### 4. **Future-Proof**

Want to switch to PostgreSQL? Just create `PostgresProcessRepository` that implements `IProcessRepository`. No changes to `ProcessManager` needed!

---

## 🔧 Implementation Details

### 1. Repository Interface (`IProcessRepository`)

```python
from abc import ABC, abstractmethod

class IProcessRepository(ABC):
    """
    Abstract interface defining the contract for process storage.
    
    Any implementation (Redis, SQL, MongoDB) must provide these methods.
    """
    
    @abstractmethod
    async def save(self, process_id: str, process_info: ProcessInfo) -> None:
        """Store a process."""
        pass
    
    @abstractmethod
    async def get(self, process_id: str) -> Optional[ProcessInfo]:
        """Retrieve a process."""
        pass
    
    # ... more methods ...
```

**Key Concept: Contract**

The interface is a **contract**: "If you implement `IProcessRepository`, you MUST provide these methods."

This allows:
- ProcessManager to depend on the interface (not concrete implementation)
- Multiple implementations (in-memory, Redis, SQL)
- Easy swapping at runtime

### 2. In-Memory Repository

```python
class InMemoryProcessRepository(IProcessRepository):
    """
    Simple dictionary-based storage for development/testing.
    
    Advantages:
    - Fast (no network calls)
    - No external dependencies
    - Easy to debug
    
    Disadvantages:
    - Data lost on restart
    - Not shared across instances
    - Limited to single machine memory
    """
    
    def __init__(self):
        self._storage: Dict[str, ProcessInfo] = {}
    
    async def save(self, process_id: str, process_info: ProcessInfo) -> None:
        self._storage[process_id] = process_info
```

**When to Use:**
- Local development
- Unit tests
- Single-instance deployments
- Prototyping

### 3. Redis Repository

```python
class RedisProcessRepository(IProcessRepository):
    """
    Redis-based persistent storage for production.
    
    Advantages:
    - Survives restarts
    - Shared across instances (horizontal scaling)
    - Fast (in-memory database)
    - Rich data structures
    
    Disadvantages:
    - Requires Redis server
    - Network latency
    - Memory costs (Redis is in-memory)
    """
```

#### Redis Data Structures Used

**1. Hash for Process Metadata**
```python
# Redis command: HSET process:{id} field value
await redis.hset(
    f"process:{process_id}",
    mapping={
        "status": "running",
        "created_at": "2025-11-08T10:00:00",
        "error": ""
    }
)
```

**Why hash?**
- Store multiple fields efficiently
- Update individual fields without fetching entire object
- Natural fit for object storage

**2. Sorted Set for Time-Based Queries**
```python
# Redis command: ZADD process_times score member
await redis.zadd(
    "process_times",
    {process_id: timestamp}
)
```

**Why sorted set?**
- Enables "get processes older than X" queries
- Used for cleanup: remove processes created before timestamp
- Efficient range queries

**3. Set for Process IDs**
```python
# Redis command: SADD process_ids member
await redis.sadd("process_ids", process_id)
```

**Why set?**
- Fast existence checks
- Easy listing of all processes
- Automatic deduplication

**4. Serialized DecisionState**
```python
# Store complex Python object
import pickle

state_bytes = pickle.dumps(decision_state)
await redis.hset(f"process:{id}", "result", state_bytes)
```

**Why pickle?**
- Preserves Python object structure (classes, nested objects)
- Works with Pydantic models
- Alternative: JSON (but loses some type info)

**Why NOT pickle?**
- Not human-readable (can't inspect in Redis CLI)
- Python-specific (can't share with non-Python services)
- Security risk (don't unpickle untrusted data)

**Production consideration:**
For microservices architecture, prefer JSON with schema validation.

#### Atomic Operations with Pipelines

```python
async def save(self, process_id: str, process_info: ProcessInfo) -> None:
    # Use pipeline for atomic multi-operation
    async with self._redis.pipeline() as pipe:
        # 1. Store process metadata
        await pipe.hset(f"process:{process_id}", mapping={...})
        
        # 2. Add to process set
        await pipe.sadd("process_ids", process_id)
        
        # 3. Add to sorted set for time-based queries
        await pipe.zadd("process_times", {process_id: timestamp})
        
        # Execute all at once (atomic)
        await pipe.execute()
```

**Why pipelines?**
- **Atomicity**: All operations succeed or fail together
- **Performance**: Single network round-trip instead of 3
- **Consistency**: No partial updates

Without pipeline:
```
1. HSET succeeds
2. Network failure
3. SADD never runs → inconsistent state!
```

With pipeline:
```
1. All operations queued
2. Execute as transaction
3. All succeed or all fail → consistent state!
```

### 4. Repository Factory

```python
def get_process_repository() -> IProcessRepository:
    """
    Factory function: automatically choose the right repository.
    
    Decision logic:
    1. Check if Redis is enabled in config
    2. Try to connect to Redis
    3. If successful → RedisProcessRepository
    4. If failed → InMemoryProcessRepository (fallback)
    """
    config = get_settings()
    
    if config.enable_redis_persistence:
        try:
            redis_client = redis.from_url(config.redis_url)
            redis_client.ping()  # Test connection
            return RedisProcessRepository(redis_client)
        except Exception as e:
            logger.warning(f"Redis unavailable, using in-memory: {e}")
            return InMemoryProcessRepository()
    
    return InMemoryProcessRepository()
```

**Why factory pattern?**
- **Automatic selection**: Right repository based on config
- **Graceful degradation**: Falls back if Redis unavailable
- **Single point of configuration**: Change in one place
- **Easy to extend**: Add more repository types easily

---

## ⚙️ Configuration

### Environment Variables

```bash
# Enable Redis persistence
ENABLE_REDIS_PERSISTENCE=true

# Redis connection (method 1: URL)
REDIS_URL=redis://localhost:6379/0

# Redis connection (method 2: individual parameters)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=secret123  # Optional
```

### Configuration Class

```python
class Settings(BaseSettings):
    # Redis persistence
    enable_redis_persistence: bool = False  # Disabled by default (safe)
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = None
    redis_url: Optional[str] = None
    
    @property
    def get_redis_url(self) -> str:
        """Build Redis URL from components if not provided."""
        if self.redis_url:
            return self.redis_url
        
        auth = f":{self.redis_password}@" if self.redis_password else ""
        return f"redis://{auth}{self.redis_host}:{self.redis_port}/{self.redis_db}"
```

---

## 🚀 Deployment Scenarios

### Scenario 1: Development (No Redis)

```yaml
# .env.development
ENABLE_REDIS_PERSISTENCE=false
```

**Result:** Uses `InMemoryProcessRepository`
- Fast development
- No external dependencies
- Data lost on restart (acceptable for dev)

### Scenario 2: Production (Single Redis Instance)

```yaml
# .env.production
ENABLE_REDIS_PERSISTENCE=true
REDIS_URL=redis://prod-redis:6379/0
```

**Architecture:**
```
┌─────────┐     ┌─────────┐     ┌─────────┐
│ Server  │────▶│  Redis  │◀────│ Server  │
│ Instance│     │ (shared)│     │ Instance│
│    1    │     └─────────┘     │    2    │
└─────────┘                     └─────────┘
```

**Benefits:**
- Shared process storage
- Horizontal scaling
- Persistent state

### Scenario 3: Production (Redis Cluster)

```yaml
# .env.production
ENABLE_REDIS_PERSISTENCE=true
REDIS_URL=redis://redis-cluster:6379/0
```

**Architecture:**
```
┌─────────┐     ┌─────────────────────┐     ┌─────────┐
│ Server  │────▶│   Redis Cluster     │◀────│ Server  │
│ Instance│     │  (sharded, replicas)│     │ Instance│
│    1    │     └─────────────────────┘     │    2    │
└─────────┘                                 └─────────┘
```

**Benefits:**
- High availability (replicas)
- Higher throughput (sharding)
- Fault tolerance

### Scenario 4: Docker Compose (Development + Redis)

```yaml
# docker-compose.yml
services:
  backend:
    environment:
      - ENABLE_REDIS_PERSISTENCE=true
      - REDIS_HOST=redis
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

**Benefits:**
- Realistic production environment
- Test persistence locally
- Easy setup

---

## 🧪 Testing Strategy

### Unit Tests (In-Memory Repository)

```python
import pytest
from backend.app.services.redis_repository import InMemoryProcessRepository

@pytest.mark.asyncio
async def test_process_save_and_get():
    """Test basic save/get operations."""
    repo = InMemoryProcessRepository()
    
    # Create test process
    process = ProcessInfo(
        process_id="test123",
        status="running",
        result=None,
        error=None,
        created_at="2025-11-08T10:00:00"
    )
    
    # Save
    await repo.save("test123", process)
    
    # Retrieve
    retrieved = await repo.get("test123")
    
    assert retrieved is not None
    assert retrieved.process_id == "test123"
    assert retrieved.status == "running"
```

**Why in-memory for unit tests?**
- Fast (no Redis startup)
- Isolated (no shared state)
- No external dependencies

### Integration Tests (Redis Repository)

```python
import pytest
import redis.asyncio as redis

@pytest.mark.asyncio
async def test_redis_process_persistence():
    """Test that processes survive Redis restart simulation."""
    # Connect to test Redis instance
    redis_client = redis.from_url("redis://localhost:6379/15")  # Use DB 15 for tests
    repo = RedisProcessRepository(redis_client)
    
    # Save process
    process = ProcessInfo(process_id="test456", status="running", ...)
    await repo.save("test456", process)
    
    # Simulate restart: create new repository instance
    redis_client2 = redis.from_url("redis://localhost:6379/15")
    repo2 = RedisProcessRepository(redis_client2)
    
    # Retrieve from new instance
    retrieved = await repo2.get("test456")
    
    assert retrieved is not None  # Survives "restart"!
    
    # Cleanup
    await redis_client.flushdb()
```

### Performance Tests

```python
import asyncio
import time

async def test_concurrent_operations():
    """Test concurrent process creation."""
    repo = get_process_repository()
    
    async def create_process(i):
        process = ProcessInfo(process_id=f"perf{i}", status="running", ...)
        await repo.save(f"perf{i}", process)
    
    # Create 100 processes concurrently
    start = time.time()
    await asyncio.gather(*[create_process(i) for i in range(100)])
    duration = time.time() - start
    
    print(f"Created 100 processes in {duration:.2f}s")
    assert duration < 5.0  # Should be fast
```

---

## 📊 Monitoring & Observability

### Key Metrics to Track

1. **Repository Type in Use**
   ```python
   repo = get_process_repository()
   print(f"Using: {type(repo).__name__}")  # InMemoryProcessRepository or RedisProcessRepository
   ```

2. **Process Counts by Status**
   ```python
   stats = await manager.get_stats()
   # {"total": 100, "running": 5, "completed": 90, "failed": 5}
   ```

3. **Redis Connection Health**
   ```python
   try:
       await redis_client.ping()
       status = "healthy"
   except Exception as e:
       status = f"unhealthy: {e}"
   ```

4. **Process Age Distribution**
   ```python
   # Processes older than 24 hours
   old_processes = await repo.list_by_time_range(
       start_time=0,
       end_time=time.time() - (24 * 3600)
   )
   print(f"Processes needing cleanup: {len(old_processes)}")
   ```

### Logging Best Practices

```python
import logging

logger = logging.getLogger(__name__)

class RedisProcessRepository:
    async def save(self, process_id: str, process_info: ProcessInfo):
        try:
            # Log operation
            logger.info(f"Saving process {process_id} with status {process_info.status}")
            
            # Perform save
            await self._redis.hset(...)
            
            logger.debug(f"Successfully saved process {process_id}")
            
        except Exception as e:
            # Log error with context
            logger.error(
                f"Failed to save process {process_id}: {e}",
                exc_info=True,  # Include stack trace
                extra={"process_id": process_id, "status": process_info.status}
            )
            raise
```

---

## 🛠️ Troubleshooting

### Issue 1: "Redis connection refused"

**Symptoms:**
```
redis.exceptions.ConnectionError: Error connecting to Redis: Connection refused
```

**Solutions:**

1. **Check Redis is running:**
   ```bash
   # Docker
   docker ps | grep redis
   
   # Local Redis
   redis-cli ping  # Should return "PONG"
   ```

2. **Check connection settings:**
   ```bash
   echo $REDIS_HOST  # Should match Redis hostname
   echo $REDIS_PORT  # Should match Redis port (default 6379)
   ```

3. **Test connection manually:**
   ```bash
   redis-cli -h localhost -p 6379 ping
   ```

### Issue 2: "Process not found after restart"

**Symptoms:**
- Process created successfully
- Server restarts
- GET /status/{id} returns 404

**Diagnosis:**
```python
# Check which repository is being used
repo = get_process_repository()
print(type(repo).__name__)

# If InMemoryProcessRepository, persistence is disabled!
```

**Solution:**
```bash
# Enable Redis persistence
export ENABLE_REDIS_PERSISTENCE=true
export REDIS_URL=redis://localhost:6379/0

# Restart application
```

### Issue 3: "Memory growing unbounded"

**Symptoms:**
- Redis memory usage constantly increasing
- Never decreases

**Root Cause:** No cleanup running!

**Solution 1: Manual cleanup**
```bash
curl -X DELETE http://localhost:8000/decisions/cleanup
```

**Solution 2: Automated cleanup (recommended)**
```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

async def cleanup_old_processes():
    manager = get_process_manager()
    cleaned = await manager.cleanup_completed(older_than_hours=24)
    logger.info(f"Cleaned up {cleaned} old processes")

# Run every hour
scheduler.add_job(cleanup_old_processes, 'interval', hours=1)
scheduler.start()
```

### Issue 4: "pickle.UnpicklingError"

**Symptoms:**
```
pickle.UnpicklingError: invalid load key, '\x00'
```

**Root Cause:** Corrupted data or version mismatch

**Solution:**
```python
# Add error handling
async def get(self, process_id: str) -> Optional[ProcessInfo]:
    result_bytes = await self._redis.hget(f"process:{process_id}", "result")
    
    if result_bytes:
        try:
            return pickle.loads(result_bytes)
        except pickle.UnpicklingError as e:
            logger.error(f"Corrupted data for {process_id}: {e}")
            # Option 1: Return None (treat as missing)
            return None
            # Option 2: Delete corrupted entry
            await self.delete(process_id)
            return None
```

---

## 🎓 Key Learning Points

### 1. **Repository Pattern Benefits**

- **Abstraction**: Business logic doesn't know about storage details
- **Testability**: Easy to mock/stub for tests
- **Flexibility**: Swap implementations without code changes
- **Maintenance**: Changes to storage don't affect business logic

### 2. **Redis as a Cache vs. Database**

**Redis characteristics:**
- In-memory (fast but limited by RAM)
- No joins, no complex queries
- Best for: caching, sessions, simple key-value, pub/sub
- Not for: complex queries, large datasets, strong ACID guarantees

### 3. **Async/Await in Python**

```python
# Synchronous (blocks thread)
def get_process(id):
    time.sleep(0.1)  # Simulating network delay
    return process

# Asynchronous (non-blocking)
async def get_process(id):
    await asyncio.sleep(0.1)  # Other tasks can run during wait
    return process
```

**Why async?**
- I/O-bound operations (network, disk) benefit greatly
- Handle many concurrent requests
- Better resource utilization

### 4. **Dependency Injection**

```python
# Bad: Hard-coded dependency
class ProcessManager:
    def __init__(self):
        self.repo = RedisProcessRepository()  # Can't change this!

# Good: Injected dependency
class ProcessManager:
    def __init__(self, repository: IProcessRepository):
        self.repo = repository  # Can be anything implementing interface!
```

**Benefits:**
- Loose coupling
- Easy testing
- Flexible configuration
- Clear dependencies

### 5. **Factory Pattern**

```python
def get_process_repository() -> IProcessRepository:
    # Encapsulates creation logic
    # Hides complexity from caller
    # Single point of configuration
    pass
```

**When to use:**
- Complex object creation
- Need to choose between implementations
- Want to centralize configuration

---

## 📖 Further Reading

### Related Design Patterns

1. **Repository Pattern**
   - [Martin Fowler: Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html)

2. **Dependency Injection**
   - [Dependency Inversion Principle (SOLID)](https://en.wikipedia.org/wiki/Dependency_inversion_principle)

3. **Factory Pattern**
   - [Factory Pattern Explained](https://refactoring.guru/design-patterns/factory-method)

### Redis Resources

1. **Redis Data Structures**
   - [Redis Data Types Documentation](https://redis.io/docs/data-types/)

2. **Redis Best Practices**
   - [Redis Memory Optimization](https://redis.io/docs/management/optimization/memory-optimization/)

3. **Redis Persistence**
   - [Redis Persistence Options](https://redis.io/docs/management/persistence/)

### Python Async

1. **AsyncIO Documentation**
   - [Python asyncio](https://docs.python.org/3/library/asyncio.html)

2. **Async Best Practices**
   - [Real Python: Async IO](https://realpython.com/async-io-python/)

---

## 🎯 Summary

This Redis persistence implementation provides:

✅ **Production-ready async process storage**
✅ **Flexible architecture (Repository Pattern)**
✅ **Graceful degradation (Redis → in-memory fallback)**
✅ **Horizontal scalability (shared Redis)**
✅ **Comprehensive documentation for learning**

Next steps:
1. Add unit tests for repository layer
2. Set up CI/CD for automated testing
3. Add monitoring/alerting for Redis health
4. Implement cleanup scheduler
5. Consider Redis clustering for high availability
