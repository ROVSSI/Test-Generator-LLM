# LLM-Assisted Test Generation for Python

This repository contains a Python framework for LLM-assisted test generation
using Category Partition, MC/DC, and State-Based Testing, plus execution-based
validation to repair incorrect generated oracles.

## Quickstart

```bash
# 1) Create venv (recommended)
python3 -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 2) Install dependencies
python -m pip install -r requirements.txt

# 3) Run tests
python -m pytest -q
```

You should see the full repository test suite pass.

## LLM-Based Test Generation

Set your API key before using the CLI:

```bash
export OPENAI_API_KEY="your-api-key"
python testgen.py llm --method category_partition src/refund_policy_code.py
```

The CLI validates every LLM-generated test case by executing the target
function or class workflow before writing pytest. If the model proposes the
wrong expected return value, misses an exception, or predicts the wrong state
transition, the tool repairs the case and prints a validation summary.

Supported methods:
- `category_partition`
- `mcdc`
- `state_based`

Example targets:
- `src/order_routing_code.py`
- `src/refund_policy_code.py`
- `src/refund_case_code.py`

All files matching `*_code.py` in `src/` are example systems under test used
to demonstrate and validate the framework. They are not part of the core
generation pipeline itself.

## Quality Checks

Local quality commands:

```bash
python -m ruff check src testgen.py tests/test_llm_generators.py tests/test_llm_validation.py
python -m mypy
python -m coverage run -m pytest -q
python -m coverage report
python -m coverage xml
cyclonedx-py requirements requirements.txt --pyproject pyproject.toml --output-format JSON --output-file sbom.json
```

The GitHub Actions workflow runs linting, type checking, tests with coverage,
and generates a CycloneDX SBOM artifact on every push and pull request.
