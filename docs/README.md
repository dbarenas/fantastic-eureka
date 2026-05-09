# ETF Advisor Agent

A multi-agent system for intelligent ETF selection and analysis using LangGraph, Neo4j, and local Ollama LLM.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ETF Advisor Agent                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────┐         ┌──────────┐         ┌──────────┐   │
│  │ Researcher│         │   Neo4j  │         │  Ollama  │   │
│  │  Agent   ├────────→│Knowledge │←────────┤  LLM     │   │
│  │          │         │  Graph   │         │          │   │
│  └──────────┘         └──────────┘         └──────────┘   │
│       ▲                     │                      ▲         │
│       │                     │                      │         │
│       └─────────────────────┴──────────────────────┘         │
│                                                               │
│  Data Flow:                                                  │
│  1. Query Neo4j for context                                 │
│  2. If insufficient, enrich via Ollama                      │
│  3. Store facts back in Neo4j                               │
│  4. Generate answer with enriched context                   │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local development)
- 4GB+ RAM (for Ollama)

### Option 1: Docker (Recommended)

```bash
# Clone and navigate
git clone <repo>
cd fantastic-eureka-feat-etf-advisor-agent

# Start services
docker-compose up

# Services will be ready at:
# - Ollama API: http://localhost:11434
# - Neo4j Browser: http://localhost:7474 (user: neo4j / pass: neo4j_pass)
```

### Option 2: Local Development

```bash
# Install dependencies
make install

# Start services (requires Docker for Neo4j + Ollama)
make docker-up

# Run agent
make run
```

## Testing

### Run All Tests
```bash
make test
# or
pytest tests/ -v
```

### Run Unit Tests Only
```bash
make test-unit
pytest tests/ -v -m "not integration"
```

### Run Integration Tests
```bash
make test-integration
pytest tests/test_integration.py -v
```

### Generate Coverage Report
```bash
make test-cov
# Opens htmlcov/index.html in browser
```

## Usage

### Command Line

```bash
# Basic usage
python -m src.main "¿Cómo selecciono un ETF para jubilación?"

# With agent ID
python -m src.main "Mi pregunta" --agent-id my-agent-001

# Verbose mode (debug logging)
python -m src.main "Mi pregunta" --verbose
```

### Python API

```python
from src.state import GraphState
from src.agents import researcher

# Create state
state = GraphState(
    agent_id='my-agent',
    question='¿Cuáles son los mejores ETFs?',
    messages=[],
    context={}
)

# Run researcher
result = researcher(state)

# Get answer
print(result.messages[-1].content)
```

## Project Structure

```
fantastic-eureka-feat-etf-advisor-agent/
├── src/
│   ├── __init__.py
│   ├── main.py           # CLI entry point
│   ├── state.py          # Data structures (GraphState, Turn)
│   ├── agents.py         # Researcher agent logic
│   ├── llm.py            # Ollama integration
│   └── neo.py            # Neo4j integration
├── tests/
│   ├── conftest.py       # Pytest fixtures
│   ├── test_state.py     # State tests
│   ├── test_llm.py       # LLM module tests
│   ├── test_neo.py       # Neo4j module tests
│   ├── test_agents.py    # Agent logic tests
│   └── test_integration.py # Full workflow tests
├── .github/workflows/
│   └── ci.yml            # GitHub Actions CI/CD
├── docker-compose.yml    # Service orchestration
├── Dockerfile            # App container
├── Makefile              # Development commands
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Development

### Code Quality

```bash
# Format code with black
make format

# Run linting
make lint

# Full CI checks (local)
make ci
```

### Environment Setup

```bash
# Copy example env
cp .env.example .env

# Edit for your setup
vim .env
```

### Available Make Commands

```bash
make help          # Show all commands
make install       # Install dependencies
make test          # Run all tests
make test-cov      # Tests + coverage
make docker-up     # Start services
make docker-down   # Stop services
make run           # Run example query
make clean         # Clean artifacts
make format        # Format code
make lint          # Check code quality
```

## API Reference

### GraphState
```python
GraphState(
    agent_id: str,           # Unique agent identifier
    question: str,           # User question
    messages: List[Turn],    # Conversation history
    context: Dict[str, Any]  # Knowledge graph context
)
```

### Turn
```python
Turn(
    role: str,       # "user" or "agent"
    agent_id: str,   # Agent identifier
    content: str     # Message content
)
```

### Researcher Agent
```python
from src.agents import researcher

result = researcher(state: GraphState) -> GraphState
```

## Configuration

### Environment Variables

```bash
# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=neo4j_pass

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3:8b
OLLAMA_TIMEOUT=300

# Logging
LOG_LEVEL=INFO
```

## Known Issues & Limitations

- **Ollama only**: No fallback to Claude API yet
- **Spanish prompts**: Localization pending
- **Single agent**: Only Researcher agent implemented
- **No persistence**: Knowledge graph resets on container restart
- **No API**: CLI-only interface currently

## Roadmap

### Phase 1: In Progress
- [x] Core researcher agent
- [x] Unit tests
- [x] Error handling & logging
- [x] Docker setup
- [ ] Code coverage > 80%
- [ ] API documentation

### Phase 2: Features
- [ ] Recommender agent (suggest specific ETFs)
- [ ] Validator agent (check recommendations)
- [ ] Multi-turn conversations
- [ ] Conversation memory in Neo4j
- [ ] FastAPI endpoint

### Phase 3: Production
- [ ] Claude API fallback
- [ ] Persistence snapshots
- [ ] Web interface
- [ ] Monitoring & observability
- [ ] Rate limiting

## Contributing

1. Create a feature branch: `git checkout -b feat/your-feature`
2. Install dev dependencies: `make install`
3. Run tests: `make test`
4. Format code: `make format`
5. Commit and push
6. Create a Pull Request

## License

[License information here]

## Support

For issues and questions:
1. Check [PROJECT_STATUS.md](PROJECT_STATUS.md) for current state
2. Run tests with `--verbose` flag
3. Check docker logs: `docker-compose logs app`
4. File an issue with test output
