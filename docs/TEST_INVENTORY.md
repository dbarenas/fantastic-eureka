# Test Inventory & Execution Guide

## Test Suite Overview

```
Total Test Cases: 38+
Mocked Dependencies: Ollama (LLM), Neo4j (Graph DB)
Test Execution Time: ~10 seconds (no external services)
Coverage Target: 80%+
```

## Test Modules

### 1. test_state.py (9 tests)
**Module**: `src/state.py`
**Coverage**: GraphState & Turn data structures

```python
# Run specific test file
pytest tests/test_state.py -v

# Individual tests:
test_turn_creation                    # Basic Turn object creation
test_turn_with_empty_content          # Edge case: empty message
test_turn_with_long_content           # Edge case: 10k+ character message
test_graph_state_creation             # Basic GraphState creation
test_graph_state_with_messages        # State with existing messages
test_graph_state_append_message       # Appending Turn objects
test_graph_state_update_context       # Updating knowledge graph context
```

### 2. test_llm.py (8 tests)
**Module**: `src/llm.py`
**Coverage**: Ollama integration, JSON parsing, retries

```python
# Run specific test file
pytest tests/test_llm.py -v

# Individual tests:
test_call_llm_success                 # Successful LLM call
test_call_llm_with_retry              # Retry logic on failure
test_call_llm_all_retries_fail        # Handles all retries failing
test_call_llm_unexpected_error        # Graceful error handling
test_call_llm_environment_variables   # Respects env vars
test_parse_valid_json                 # Parse standard JSON
test_parse_json_with_surrounding_text # Extract JSON from prose
test_parse_invalid_json               # Handle malformed JSON
test_parse_no_json_in_text            # No JSON in response
test_parse_nested_json                # Complex nested structures
test_parse_json_array                 # Array parsing
test_parse_multiline_json             # Multi-line formatting
```

### 3. test_neo.py (8 tests)
**Module**: `src/neo.py`
**Coverage**: Neo4j integration, fact storage, context retrieval

```python
# Run specific test file
pytest tests/test_neo.py -v

# Individual tests:
test_get_agent_context_success        # Retrieve facts successfully
test_get_agent_context_no_facts       # Handle empty context
test_get_agent_context_driver_not_initialized  # Missing driver
test_get_agent_context_database_error # Connection errors
test_write_fact_success               # Write fact to graph
test_write_fact_with_different_factors # Different classifications
test_write_fact_none_result           # Handle None response
test_write_fact_driver_not_initialized # Missing driver
test_write_fact_database_error        # Write errors
test_classify_rel_query_structure     # Query validation
test_get_context_query_structure      # Query validation
```

### 4. test_agents.py (6 tests)
**Module**: `src/agents.py`
**Coverage**: Researcher agent logic, enrichment, context management

```python
# Run specific test file
pytest tests/test_agents.py -v

# Individual tests:
test_researcher_with_existing_context        # Use cached facts
test_researcher_enriches_with_llm            # Enrichment workflow
test_researcher_maintains_agent_id           # Agent ID preservation
test_researcher_appends_turn_correctly       # Message tracking
test_researcher_with_empty_enrichment        # Invalid JSON handling
test_researcher_handles_malformed_json       # Graceful degradation
```

### 5. test_integration.py (7+ tests)
**Module**: Full workflow integration
**Coverage**: Complete researcher workflow, edge cases, error conditions

```python
# Run specific test file
pytest tests/test_integration.py -v

# Individual tests:
test_full_researcher_workflow               # Complete happy path
test_researcher_with_malformed_json_response # Invalid JSON handling
test_researcher_with_large_context          # 50+ facts
test_researcher_with_unicode_content        # Special characters
test_researcher_empty_question              # Edge case: empty input
test_researcher_very_long_question          # Edge case: long input
```

## Running Tests

### Quick Tests (No Setup Required)

```bash
# All tests (38+)
make test

# Or directly with pytest
pytest tests/ -v
```

### Run Specific Test Category

```bash
# Unit tests only (excludes integration)
make test-unit
pytest tests/ -v -m "not integration"

# Integration tests
make test-integration
pytest tests/test_integration.py -v

# Only tests marked as "slow"
pytest tests/ -v -m slow
```

### Run Specific Test File

```bash
# State module tests
pytest tests/test_state.py -v

# LLM module tests
pytest tests/test_llm.py -v

# Neo4j module tests
pytest tests/test_neo.py -v

# Agent logic tests
pytest tests/test_agents.py -v

# Full workflow tests
pytest tests/test_integration.py -v
```

### Run Specific Test

```bash
# Single test
pytest tests/test_agents.py::TestResearcher::test_researcher_with_existing_context -v

# Pattern matching
pytest tests/test_llm.py -k "parse" -v
```

### With Coverage Report

```bash
# Generate coverage
make test-cov

# Or directly
pytest tests/ --cov=src --cov-report=html --cov-report=term-missing

# View HTML report
open htmlcov/index.html
```

### With Verbose Output

```bash
# Show print statements
pytest tests/ -v -s

# Show logging
pytest tests/ -v --log-cli-level=DEBUG

# Show local variables on failure
pytest tests/ -v -l
```

### Parallel Execution (Fast)

```bash
# Install pytest-xdist first
pip install pytest-xdist

# Run in parallel
pytest tests/ -n auto
```

## Test Structure

### Unit Tests
```
Purpose: Test individual functions/modules in isolation
Dependencies: Mocked (no external services)
Execution Time: < 0.5s per test
Total: ~30 tests
```

### Integration Tests
```
Purpose: Test full workflows with realistic data
Dependencies: Mocked services
Execution Time: < 1s per test
Total: ~7 tests
```

## Mock Strategy

All tests use mocked services (no Docker required):

```python
# In tests/conftest.py - shared fixtures

@pytest.fixture
def mock_neo4j_driver():
    """Mock Neo4j for testing without database"""
    
@pytest.fixture
def mock_ollama_client():
    """Mock Ollama for testing without LLM service"""

@pytest.fixture
def sample_graph_state():
    """Sample state for testing"""
```

## Expected Test Output

```bash
$ make test

tests/test_state.py::TestTurn::test_turn_creation PASSED
tests/test_state.py::TestTurn::test_turn_with_empty_content PASSED
tests/test_state.py::TestTurn::test_turn_with_long_content PASSED
tests/test_state.py::TestGraphState::test_graph_state_creation PASSED
...
tests/test_integration.py::TestResearcherIntegration::test_full_researcher_workflow PASSED
tests/test_integration.py::TestResearcherEdgeCases::test_researcher_empty_question PASSED

========================= 38 passed in 2.34s ==========================
```

## Coverage Example

```bash
$ make test-cov

Name                 Stmts   Miss  Cover   Missing
------------------------------------------------------
src/agents.py           45      2    96%    42, 78
src/llm.py              25      1    96%    30
src/main.py             35      3    91%    15-17, 40
src/neo.py              52      4    92%    25, 68, 85
src/state.py             8      0   100%
------------------------------------------------------
TOTAL                  165      10   94%
```

## Common Test Scenarios

### Scenario 1: Test Failed Connection Retry
```python
# In tests/test_llm.py::test_call_llm_with_retry
mock_client.chat.side_effect = [
    ollama.RequestError("Connection failed"),
    {'message': {'content': 'Success on retry'}}
]
result = call_llm('Test prompt', retries=2)
assert result == 'Success on retry'
```

### Scenario 2: Test JSON Parsing Robustness
```python
# In tests/test_llm.py::test_parse_json_with_surrounding_text
text = "Here is some JSON: {\"key\": \"value\"} and more text."
result = parse_json_from_text(text)
assert result == {"key": "value"}
```

### Scenario 3: Test Agent Enrichment
```python
# In tests/test_agents.py::test_researcher_enriches_with_llm
mock_context.side_effect = [[], [enriched_facts]]
result = researcher(state)
assert mock_llm.call_count == 2  # Enrichment + Answer
```

## Debugging Tests

### See What's Happening
```bash
# Run with print statements visible
pytest tests/test_agents.py::TestResearcher::test_researcher_with_existing_context -s

# Show variables on failure
pytest tests/ -l

# Full traceback
pytest tests/ --tb=long
```

### Check Mock Calls
```python
# In your test
mock_llm.assert_called_once()
mock_neo.call_count == 3
mock_driver.session.assert_called()
```

## Continuous Integration

The GitHub Actions workflow automatically:

1. Installs dependencies
2. Runs linting (flake8)
3. Runs all unit tests
4. Runs integration tests with real Neo4j
5. Uploads coverage to Codecov
6. Builds Docker image

```yaml
# .github/workflows/ci.yml
- Triggers on: push to main/dev/feat-*, pull requests
- Python versions: 3.9, 3.10, 3.11
- Services: Neo4j 5.25
```

## Best Practices

### When Adding New Code
```bash
1. Write test first (TDD approach)
2. Run make test-unit to verify
3. Implement feature
4. Run make test to verify all pass
5. Check coverage: make test-cov
6. Format: make format
7. Commit
```

### Before Pushing
```bash
make ci  # Runs: clean, install, test, lint
```

### After Failing Tests
```bash
# See what failed
pytest tests/test_agents.py -v

# Debug it
pytest tests/test_agents.py::TestResearcher -s --tb=short

# Check if it's timing
pytest tests/ --durations=10
```

## Test Maintenance

### Adding New Tests

Create file: `tests/test_new_module.py`

```python
import pytest
from unittest.mock import patch
from src.new_module import new_function

class TestNewModule:
    @patch('src.new_module.dependency')
    def test_new_function(self, mock_dep):
        mock_dep.return_value = 'test'
        result = new_function()
        assert result == 'test'
```

Then run:
```bash
pytest tests/test_new_module.py -v
```

### Updating Fixtures

Edit `tests/conftest.py` to add/modify shared fixtures:

```python
@pytest.fixture
def new_fixture():
    return "new value"
```

Use in tests:
```python
def test_something(new_fixture):
    assert new_fixture == "new value"
```

---

**Ready to test!** 🧪 Run `make test` to get started.
