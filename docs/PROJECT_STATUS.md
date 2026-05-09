# ETF Advisor Agent - Project Status

## 🏗️ Current Architecture

**Stack:**
- **LLM**: Ollama (local, llama3:8b)
- **Knowledge Graph**: Neo4j (stores facts classified by factors)
- **Framework**: LangGraph + LangChain
- **Language**: Python 3.11

**Key Components:**
1. **State** (`state.py`) - `GraphState` with agent_id, question, messages, context
2. **Researcher Agent** (`agents.py`) - Retrieves Neo4j context → enriches via LLM → answers question
3. **Neo4j KB** (`neo.py`) - Stores facts linked to factors (Perfil/Producto/Operativa)
4. **LLM** (`llm.py`) - Calls Ollama service

## 📋 Current Workflow
1. User asks a question (via CLI arg)
2. Researcher fetches agent context from Neo4j
3. If insufficient data, calls LLM to generate ETF selection factors
4. Writes new facts back to Neo4j
5. Calls LLM again with full context to answer the question

## ⚠️ Issues & Gaps

### Code Issues
- **Missing imports**: `requirements.txt` doesn't include langchain-community, langchain-core
- **Error handling**: Minimal exception handling in agent logic
- **JSON parsing**: Regex-based JSON extraction is fragile
- **Type hints**: Missing/incomplete throughout
- **Logging**: No debug/info logging for troubleshooting

### Testing
- **No tests** - no unit tests, integration tests, or mock setups
- **Hard-coded prompts** - all in Spanish, no i18n
- **CLI-only** - no API, no web interface, hard to iterate

### Architecture
- **Single agent**: Only `researcher` exists, no validator/recommender/etc.
- **No persistence**: Knowledge graph ephemeral after restart
- **No multi-turn**: State doesn't support conversation history
- **Ollama only**: No fallback to Claude API

## 🎯 Next Steps to Resume

### Phase 1: Fix & Test (Immediate)
- [ ] Add missing dependencies to `requirements.txt`
- [ ] Create `tests/` directory with pytest suite
- [ ] Mock Ollama/Neo4j for unit tests
- [ ] Add CI/CD (GitHub Actions)
- [ ] Improve error handling

### Phase 2: Enhance Agent (Features)
- [ ] Add **Recommender Agent** (suggests specific ETFs based on profile)
- [ ] Add **Validator Agent** (checks recommendations against rules)
- [ ] Implement multi-turn conversation in state
- [ ] Add conversation memory to Neo4j
- [ ] Better prompt engineering for ETF analysis

### Phase 3: Integration (Production Ready)
- [ ] Add FastAPI endpoint for agent queries
- [ ] Add Claude API fallback (when Ollama unavailable)
- [ ] Add persistence/snapshots of knowledge graph
- [ ] Add logging + monitoring
- [ ] Containerize with proper health checks

## 🚀 Quick Start (Current)
```bash
docker-compose up
# Runs researcher agent with: "Explica los tres factores para elegir ETFs"
```

## 🐛 Potential Quick Fixes
1. **requirements.txt** - Add: `langchain-core`, `langchain-community`, `pydantic`
2. **llm.py** - Add timeout + retry logic for Ollama
3. **agents.py** - Improve JSON extraction (use json.loads with fallback)
4. **neo.py** - Add connection pooling + timeout
5. **main.py** - Add --verbose flag for debug logging
