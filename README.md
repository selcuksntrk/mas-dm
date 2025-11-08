# Multi-Agent Decision Making API

A sophisticated AI-powered decision-making system using multiple agents in a collaborative workflow. The system analyzes decisions through trigger identification, root cause analysis, scope definition, goal establishment, alternative generation, and comprehensive evaluation.

## 🌟 Features

- **Multi-Agent Architecture**: 10 specialized decision agents + 9 evaluation agents
- **Graph-Based Workflow**: Structured decision pipeline with evaluation loops
- **Async Processing**: Background decision processing with status tracking
- **Redis Persistence**: Production-ready persistent storage for async processes (NEW! ✨)
- **Repository Pattern**: Clean architecture with flexible storage backends
- **REST API**: FastAPI-based API with automatic documentation
- **Docker Support**: Containerized deployment with Docker Compose
- **Horizontal Scaling**: Multiple instances sharing Redis storage

## 🚀 Quick Start

### Option 1: Docker (Recommended)

**Prerequisites:**
- Docker Desktop installed ([Download](https://docs.docker.com/get-docker/))

**Setup:**
```bash
# 1. Clone the repository
git clone <your-repo-url>
cd PydanticAI_v2

# 2. Create environment file
cp .env.example .env

# 3. Edit .env and add your API keys
# OPENAI_API_KEY=sk-your-key-here
# GITHUB_TOKEN=ghp-your-token-here (optional)

# 4. Start the application
./docker-start.sh

# Or manually:
docker-compose up
```

**Access the API:**
- API: http://localhost:8001
- Interactive Docs: http://localhost:8001/docs
- Health Check: http://localhost:8001/health

**Stop the application:**
```bash
./docker-stop.sh
# Or: docker-compose down
```

### Option 2: Local Development

**Prerequisites:**
- Python 3.13+
- UV package manager ([Install](https://github.com/astral-sh/uv))

**Setup:**
```bash
# 1. Install dependencies
uv sync

# 2. Set environment variables
export OPENAI_API_KEY=sk-your-key-here
export GITHUB_TOKEN=ghp-your-token-here  # optional

# 3. Start the backend API
cd backend
uv run uvicorn app.main:app --port 8001 --reload
```

## 📚 Documentation

- **[Docker Guide](DOCKER_GUIDE.md)** - Comprehensive Docker deployment guide
- **[API Documentation](http://localhost:8001/docs)** - Interactive API docs (when running)
- **[Migration Progress](MIGRATION_PROGRESS.md)** - Development progress tracking
- **[Testing Results](PHASE4_TESTING_RESULTS.md)** - Test results and performance metrics

## 🏗️ Architecture

### Project Structure

```
PydanticAI_v2/
├── backend/                    # New backend (clean architecture)
│   ├── app/
│   │   ├── api/               # API routes
│   │   │   ├── routes/        # Endpoint definitions
│   │   │   │   ├── decisions.py  # Decision endpoints
│   │   │   │   ├── graph.py      # Graph visualization
│   │   │   │   └── health.py     # Health checks
│   │   ├── core/              # Core business logic
│   │   │   ├── agents/        # Decision & evaluation agents
│   │   │   ├── graph/         # Graph execution
│   │   │   └── prompts/       # Agent system prompts
│   │   ├── models/            # Data models
│   │   │   ├── domain.py      # Domain models
│   │   │   ├── requests.py    # API request models
│   │   │   └── responses.py   # API response models
│   │   ├── services/          # Service layer
│   │   │   ├── decision_service.py   # Decision orchestration
│   │   │   └── process_manager.py    # Async process management
│   │   ├── config.py          # Configuration
│   │   └── main.py            # FastAPI application
│   ├── Dockerfile             # Container definition
│   └── README.md              # Backend documentation
├── src/                       # Legacy application
├── docker-compose.yml         # Multi-container orchestration
├── docker-start.sh           # Helper script to start Docker
├── docker-stop.sh            # Helper script to stop Docker
├── test_backend_api.py       # API test suite
└── .env.example              # Environment variables template
```

### System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Client/Frontend                       │
└───────────────────────┬─────────────────────────────────┘
                        │ HTTP/REST
┌───────────────────────▼─────────────────────────────────┐
│                     API Layer (FastAPI)                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │  Health     │  │   Graph     │  │  Decisions  │    │
│  │  Routes     │  │   Routes    │  │   Routes    │    │
│  └─────────────┘  └─────────────┘  └─────────────┘    │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│                   Service Layer                          │
│  ┌──────────────────┐      ┌───────────────────────┐   │
│  │ DecisionService  │      │  ProcessManager       │   │
│  │ (Orchestration)  │◄────►│  (Async Processes)    │   │
│  └──────────────────┘      └───────────────────────┘   │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│                     Core Layer                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   Agents    │  │    Graph    │  │   Prompts   │    │
│  │  (10+9)     │  │  Executor   │  │ Templates   │    │
│  └─────────────┘  └─────────────┘  └─────────────┘    │
└─────────────────────────────────────────────────────────┘
```

### Decision Workflow

```
GetDecision → IdentifyTrigger ⇄ Evaluate
            ↓
    AnalyzeRootCause ⇄ Evaluate
            ↓
    ScopeDefinition ⇄ Evaluate
            ↓
       Drafting ⇄ Evaluate
            ↓
    EstablishGoals ⇄ Evaluate
            ↓
    IdentifyInformationNeeded ⇄ Evaluate
            ↓ (optional retrieval loop)
      UpdateDraft ⇄ Evaluate
            ↓
    GenerationOfAlternatives ⇄ Evaluate
            ↓
        Result ⇄ Evaluate
            ↓
          END
```

## 🧪 Testing

### Run Test Suite

```bash
# Quick tests (no AI execution)
uv run python test_backend_api.py quick

# Full tests with synchronous decision
uv run python test_backend_api.py full

# Full tests with async decision
uv run python test_backend_api.py full-async

# Test against custom URL
uv run python test_backend_api.py quick http://localhost:8001
```

### Manual Testing

```bash
# Health check
curl http://localhost:8001/health

# Graph structure
curl http://localhost:8001/graph/structure

# Run a decision
curl -X POST http://localhost:8001/decisions/run \
  -H "Content-Type: application/json" \
  -d '{"decision_query": "Should I learn Docker?"}'
```

## 📊 API Endpoints

### Health & Info
- `GET /` - API information
- `GET /health` - Health check

### Graph Visualization
- `GET /graph/mermaid` - Get Mermaid diagram code
- `GET /graph/structure` - Get graph structure metadata

### Decision Making
- `POST /decisions/run` - Run decision synchronously
- `POST /decisions/start` - Start decision asynchronously
- `GET /decisions/status/{id}` - Get async process status
- `GET /decisions/processes` - List all processes
- `DELETE /decisions/cleanup` - Clean up completed processes
- `POST /decisions/cli` - Debug mode with persistence

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with:

```bash
# Required
OPENAI_API_KEY=sk-your-key-here

# Optional
GITHUB_TOKEN=ghp-your-token-here
MODEL_NAME=gpt-4o-mini
EVALUATION_MODEL_NAME=gpt-4o-mini
LOG_LEVEL=INFO

# Redis (future feature)
REDIS_HOST=redis
REDIS_PORT=6379
```

### Available Models

- `gpt-4o-mini` - Fast, cost-effective, good quality (default)
- `gpt-4o` - Best quality, slower, more expensive
- `gpt-4-turbo` - Balanced performance
- `gpt-3.5-turbo` - Fastest, cheapest, lower quality

## 🔄 Development

### Project Phases

- ✅ **Phase 1**: Directory structure and setup
- ✅ **Phase 2**: Core components migration (agents, graph)
- ✅ **Phase 3**: Service layer & API refactoring
- ✅ **Phase 4**: Testing & validation
- ⏭️ **Phase 5**: Parallel testing (skipped)
- 🔄 **Phase 6**: Docker & deployment (in progress)
- ⏳ **Phase 7**: Redis persistence
- ⏳ **Phase 8**: CI/CD & monitoring

### Recent Updates

- ✅ Backend API fully functional (6/6 tests passing)
- ✅ Clean architecture implementation
- ✅ Docker containerization
- ✅ Comprehensive documentation
- ✅ Test suite with quick/full modes

## 🐛 Known Issues

- Async processes use in-memory storage (lost on restart)
  - **Solution**: Redis persistence coming in Phase 7
- Long execution times (~97 seconds for full decision)
  - **Expected**: Complex multi-agent workflow with LLM calls
  - **Future**: Caching and optimization planned

## 📈 Performance

### Benchmarks (Current)

- **Synchronous Decision**: ~97 seconds
- **API Response Time**: < 50ms (non-decision endpoints)
- **Process Creation**: < 100ms
- **Health Check**: < 10ms

### Optimization Roadmap

1. Response caching for repeated queries
2. Parallel agent execution where possible
3. Streaming responses for real-time updates
4. Model optimization (prompt compression)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `uv run python test_backend_api.py full`
5. Submit a pull request

## 📄 License

[Your License Here]

## 🙏 Acknowledgments

- Built with [Pydantic AI](https://ai.pydantic.dev/)
- API framework: [FastAPI](https://fastapi.tiangolo.com/)
- Package management: [UV](https://github.com/astral-sh/uv)
- Containerization: [Docker](https://www.docker.com/)

## 📞 Support

- 📖 [Full Docker Guide](docs/DOCKER_GUIDE.md)
- � [Redis Persistence Guide](docs/REDIS_PERSISTENCE.md)
- ⚡ [Redis Quick Start](docs/REDIS_QUICK_START.md)
- 📋 [Phase 7 Summary](docs/PHASE_7_SUMMARY.md)
- �🐛 [Report Issues](https://github.com/your-repo/issues)
- 💬 [Discussions](https://github.com/your-repo/discussions)

## 📚 Documentation

### Architecture & Design
- [Redis Persistence Architecture](docs/REDIS_PERSISTENCE.md) - Complete guide to Repository Pattern implementation
- [Phase 7 Implementation Summary](docs/PHASE_7_SUMMARY.md) - Redis persistence feature details

### Quick Guides
- [Redis Quick Start](docs/REDIS_QUICK_START.md) - Get Redis running in 5 minutes
- [Docker Guide](docs/DOCKER_GUIDE.md) - Comprehensive Docker deployment guide

---

**Built with ❤️ using Pydantic AI and FastAPI**
