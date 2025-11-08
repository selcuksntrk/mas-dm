# Multi-Agent Decision Making API - Backend

A sophisticated multi-agent system for structured decision-making, built with FastAPI, Pydantic AI, and clean architecture principles.

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- UV package manager

### Installation

```bash
# Navigate to backend directory
cd backend

# Install dependencies
uv sync

# Copy configuration (if not already present)
cp ../src/config.ini ./config.ini
```

### Running the API

**Option 1: Using run script**
```bash
uv run python run.py
```

**Option 2: Direct uvicorn**
```bash
uv run uvicorn app.main:app --port 8001 --reload
```

**Option 3: From main.py**
```bash
uv run python app/main.py
```

The API will be available at:
- **API**: http://localhost:8001
- **Interactive Docs**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

## 📚 API Documentation

### Endpoints

#### Health & Info
- `GET /` - API information and available endpoints
- `GET /health` - Health check

#### Graph Visualization
- `GET /graph/mermaid` - Get Mermaid diagram code
- `GET /graph/structure` - Get graph metadata

#### Decision Making
- `POST /decisions/run` - Run decision process synchronously
- `POST /decisions/start` - Start decision process asynchronously
- `GET /decisions/status/{process_id}` - Check process status
- `POST /decisions/cli` - Run with persistence (debug mode)
- `DELETE /decisions/cleanup` - Clean up completed processes
- `GET /decisions/processes` - List all processes

### Example Usage

**Synchronous Decision**
```bash
curl -X POST http://localhost:8001/decisions/run \
  -H "Content-Type: application/json" \
  -d '{
    "decision_query": "Should I switch careers from engineering to product management?"
  }'
```

**Asynchronous Decision**
```bash
# Start process
PROCESS_ID=$(curl -X POST http://localhost:8001/decisions/start \
  -H "Content-Type: application/json" \
  -d '{"decision_query": "Should I invest in renewable energy?"}' \
  | jq -r '.process_id')

# Check status
curl http://localhost:8001/decisions/status/$PROCESS_ID
```

**Get Graph Visualization**
```bash
curl http://localhost:8001/graph/mermaid
```

## 🏗️ Architecture

### Directory Structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration management
│   ├── api/
│   │   └── routes/
│   │       ├── health.py       # Health endpoints
│   │       ├── graph.py        # Graph visualization
│   │       └── decisions.py    # Decision endpoints
│   ├── services/
│   │   ├── decision_service.py # Decision orchestration
│   │   └── process_manager.py  # Async process management
│   ├── core/
│   │   ├── agents/
│   │   │   ├── decision_agents.py  # 10 decision agents
│   │   │   └── evaluator_agents.py # 8 evaluator agents
│   │   ├── graph/
│   │   │   ├── nodes.py        # 19 graph nodes
│   │   │   └── executor.py     # Graph execution
│   │   └── prompts/
│   │       └── templates/      # System prompts
│   ├── models/
│   │   ├── requests.py         # Request schemas
│   │   ├── responses.py        # Response schemas
│   │   └── domain.py           # Domain entities
│   └── utils/
│       └── helpers.py          # Utility functions
├── run.py                      # Run script
└── pyproject.toml              # Dependencies
```

### Layers

1. **API Layer** (`app/api/routes/`)
   - HTTP endpoints
   - Request/response handling
   - Input validation

2. **Service Layer** (`app/services/`)
   - Business logic orchestration
   - Process management
   - Result extraction

3. **Core Layer** (`app/core/`)
   - Decision agents
   - Evaluator agents
   - Graph execution

4. **Models** (`app/models/`)
   - Request/response schemas
   - Domain entities
   - Data validation

## 🔧 Configuration

Configuration is managed through:
1. Environment variables
2. `.env` file
3. `config.ini` file

### Key Settings

```ini
[api]
model = openai:gpt-4o  # Main decision model
evaluation_model = openai:gpt-4o-mini  # Evaluator model
```

See `config.py` for all available settings.

## 🧪 Testing

### Manual Testing

1. Start the API:
```bash
uv run uvicorn app.main:app --port 8001 --reload
```

2. Open interactive docs:
```
http://localhost:8001/docs
```

3. Test endpoints using the Swagger UI

### Automated Testing

```bash
# Run tests (when available)
uv run pytest

# Run with coverage
uv run pytest --cov=app
```

## 📈 Monitoring

### Process Statistics

```bash
# Get process stats
curl http://localhost:8001/decisions/processes
```

### Cleanup

```bash
# Clean up completed/failed processes
curl -X DELETE http://localhost:8001/decisions/cleanup
```

## 🔍 Debugging

### CLI Mode with Persistence

For debugging, use the CLI mode which saves execution history:

```bash
curl -X POST http://localhost:8001/decisions/cli \
  -H "Content-Type: application/json" \
  -d '{"decision_query": "Should I switch careers?"}'
```

This creates a `decision_graph.json` file with the complete execution history.

## 🚦 Development

### Hot Reload

The API supports hot reload for development:

```bash
uv run uvicorn app.main:app --port 8001 --reload
```

Changes to Python files will automatically restart the server.

### Adding New Endpoints

1. Create route handler in `app/api/routes/`
2. Add business logic to `app/services/`
3. Register router in `app/main.py`

### Adding New Agents

1. Add agent to `app/core/agents/decision_agents.py`
2. Add to `DECISION_AGENTS` registry
3. Create corresponding evaluator in `evaluator_agents.py`
4. Add nodes to `app/core/graph/nodes.py`

## 📝 Decision Workflow

The system follows a structured workflow:

1. **Analysis Phase**
   - Identify trigger
   - Analyze root cause
   - Define scope

2. **Drafting Phase**
   - Create initial draft
   - Establish SMART goals

3. **Information Gathering**
   - Identify needed information
   - Retrieve additional data
   - Update draft

4. **Alternatives Phase**
   - Generate alternatives
   - Evaluate options

5. **Decision Phase**
   - Select best option
   - Provide justification
   - Suggest alternative

Each phase includes agent execution and evaluator validation with feedback loops.

## 🛠️ Technology Stack

- **Framework**: FastAPI 0.115.0+
- **AI Framework**: Pydantic AI 1.12.0+
- **Graph Engine**: Pydantic Graph
- **Validation**: Pydantic 2.11.0+
- **Server**: Uvicorn
- **Package Manager**: UV

## 📚 Documentation

- **API Docs**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc
- **Architecture**: See `ARCHITECTURE.md` in project root
- **Migration**: See `MIGRATION_PROGRESS.md` in project root

## 🤝 Contributing

1. Follow clean architecture principles
2. Add type hints to all functions
3. Document all public APIs
4. Write tests for new features
5. Update API documentation

## 📄 License

See project root for license information.

## 🔗 Related

- **Old API**: See `../src/app.py` (legacy implementation)
- **Migration Guide**: See `MIGRATION_PROGRESS.md`
- **Phase Documentation**: See `PHASE*.md` files
