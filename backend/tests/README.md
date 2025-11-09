# Backend Tests

Comprehensive test suite for the Multi-Agent Decision Making backend API.

## Test Structure

```
tests/
├── __init__.py                 # Test package marker
├── conftest.py                 # Shared fixtures and configuration
├── test_api_health.py          # Health endpoint tests
├── test_api_graph.py           # Graph visualization tests
├── test_api_decisions.py       # Decision-making API tests
├── test_repository.py          # Repository layer tests
└── test_process_manager.py     # Process manager service tests
```

## Running Tests

### Run All Tests

```bash
# From backend directory
pytest

# With coverage report
pytest --cov=app --cov-report=html
```

### Run Specific Test Files

```bash
# Health endpoint tests
pytest tests/test_api_health.py

# Repository tests
pytest tests/test_repository.py

# Process manager tests
pytest tests/test_process_manager.py
```

### Run by Marker

Tests are organized with markers for selective execution:

```bash
# Run only unit tests (fast)
pytest -m unit

# Run integration tests
pytest -m integration

# Run slow tests (includes real AI API calls)
pytest -m slow

# Run Redis-specific tests
pytest -m redis

# Exclude slow tests
pytest -m "not slow"
```

### Verbose Output

```bash
# Show test names and output
pytest -v

# Show print statements
pytest -s

# Both verbose and show output
pytest -vs
```

## Test Categories

### Unit Tests (`@pytest.mark.unit`)

Fast, isolated tests that don't make external API calls:
- Health endpoint validation
- Graph structure tests
- Repository CRUD operations
- Process manager logic

**Run time:** < 5 seconds

```bash
pytest -m unit
```

### Integration Tests (`@pytest.mark.integration`)

Tests that verify component integration:
- API endpoint integration
- Process lifecycle management
- Repository with process manager

**Run time:** 5-30 seconds

```bash
pytest -m integration
```

### Slow Tests (`@pytest.mark.slow`)

Tests that make real AI API calls and take several minutes:
- Full decision execution (`test_decision_run_sync_full`)
- Complete process workflow (`test_process_manager_execute_full`)

**Run time:** 3-10 minutes per test

```bash
# Only run slow tests
pytest -m slow

# Skip slow tests (recommended for CI)
pytest -m "not slow"
```

### Redis Tests (`@pytest.mark.redis`)

Tests requiring Redis connection:
- RedisProcessRepository tests
- Redis persistence validation

**Requirements:** Redis server must be running

```bash
# Start Redis with Docker
docker compose up -d redis

# Run Redis tests
pytest -m redis
```

## Test Fixtures

Located in `conftest.py`:

### Client Fixtures

- **`test_client`**: Synchronous FastAPI TestClient
- **`async_client`**: Asynchronous httpx AsyncClient

### Repository Fixtures

- **`in_memory_repository`**: Clean InMemoryProcessRepository instance
- **`process_manager`**: ProcessManager with in-memory repository

### Data Fixtures

- **`sample_decision_query`**: Single test query
- **`sample_decision_queries`**: List of test queries
- **`mock_decision_result`**: Sample decision result

## Example Usage

### Test a Specific Function

```python
import pytest
from backend.app.services.redis_repository import InMemoryProcessRepository

@pytest.mark.unit
@pytest.mark.asyncio
async def test_repository_save():
    repo = InMemoryProcessRepository()
    # ... your test code
```

### Use Fixtures

```python
@pytest.mark.unit
def test_health(test_client):
    response = test_client.get("/health")
    assert response.status_code == 200
```

### Async Tests

```python
@pytest.mark.unit
@pytest.mark.asyncio
async def test_async_endpoint(async_client):
    response = await async_client.get("/health")
    assert response.status_code == 200
```

## Coverage

Generate coverage reports:

```bash
# Terminal report
pytest --cov=app --cov-report=term-missing

# HTML report (opens in browser)
pytest --cov=app --cov-report=html
open htmlcov/index.html
```

Coverage configuration is in `pyproject.toml` under `[tool.coverage]`.

## Continuous Integration

Tests are configured for GitHub Actions (see Phase 8 for CI/CD setup).

Recommended CI configuration:
```yaml
- name: Run tests
  run: |
    cd backend
    pytest -m "not slow" --cov=app --cov-report=xml
```

## Writing New Tests

### 1. Follow Naming Conventions

- Test files: `test_*.py`
- Test functions: `test_*`
- Test classes: `Test*`

### 2. Use Appropriate Markers

```python
@pytest.mark.unit          # Fast, isolated tests
@pytest.mark.integration   # Component integration tests
@pytest.mark.slow          # Tests with real API calls
@pytest.mark.redis         # Requires Redis
```

### 3. Use Type Hints

```python
def test_example(test_client: TestClient) -> None:
    """Test description."""
    # Test implementation
```

### 4. Add Docstrings

```python
def test_health_endpoint(test_client: TestClient):
    """
    Test the health check endpoint returns healthy status.
    
    Args:
        test_client: FastAPI test client fixture
    """
    # Test implementation
```

### 5. Organize with AAA Pattern

```python
def test_example():
    # Arrange - Set up test data
    query = "Should I test this?"
    
    # Act - Execute the code being tested
    response = client.post("/endpoint", json={"query": query})
    
    # Assert - Verify the results
    assert response.status_code == 200
    assert "result" in response.json()
```

## Troubleshooting

### Import Errors

Make sure the backend is installed in development mode:
```bash
cd backend
uv pip install -e ".[dev]"
```

### Redis Connection Errors

Start Redis before running Redis tests:
```bash
docker compose up -d redis
```

### Slow Test Timeouts

Increase timeout for slow tests:
```python
@pytest.mark.asyncio
async def test_slow_operation(async_client):
    response = await async_client.post(
        "/decisions/run",
        json={"decision_query": "test"},
        timeout=300.0  # 5 minutes
    )
```

### Async Test Warnings

Make sure pytest-asyncio is installed and tests are marked:
```python
@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function()
    assert result is not None
```

## Best Practices

1. **Keep unit tests fast** - Mock external dependencies
2. **Use fixtures** - Reuse common test setup
3. **Test one thing** - Each test should verify one specific behavior
4. **Clear assertions** - Use descriptive assertion messages
5. **Clean up** - Use fixtures to ensure test isolation
6. **Document** - Add docstrings explaining what each test verifies

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Coverage.py](https://coverage.readthedocs.io/)
