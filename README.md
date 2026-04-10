# LLM-Assisted Unit Test Generator — Phase 1 (Setup)

This repo is the starting scaffold for the project.
For Phase 1 we verify the environment using a tiny sample function and a basic pytest test.

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
python testgen.py llm --method category_partition src/complex_code.py
```

The CLI now validates every LLM-generated test case by executing the target
function before writing pytest. If the model proposes the wrong expected
return value or misses an exception, the tool repairs the case and prints a
validation summary.
