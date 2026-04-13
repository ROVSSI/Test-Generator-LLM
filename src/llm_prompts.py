CATEGORY_PARTITION_PROMPT = """
You are a software testing expert.

Apply the CATEGORY PARTITION testing technique.

IMPORTANT RULES:
- Output ONLY raw JSON.
- Do NOT include explanations.
- Do NOT use markdown.
- Do NOT include backticks.
- For normal cases, include the exact return value in `expected_return` and set `expected_exception` to null.
- For exception cases, set `expected_return` to null and `expected_exception` to the built-in exception class name.

Return ONLY valid JSON following this structure:
{{
  "function": "...",
  "parameters": {{
    "parameter_name": {{
      "categories": {{
        "category": ["choice"]
      }}
    }}
  }},
  "invalid_combinations": [],
  "test_cases": [
    {{
      "id": "TC1",
      "description": "...",
      "inputs": {{"parameter_name": "concrete argument value"}},
      "expected_behavior": "normal | exception",
      "expected_return": "exact return value or null",
      "expected_exception": "ValueError or null"
    }}
  ]
}}

Function under test:
-------------------
{function_code}
"""

MCDC_PROMPT = """
You are a software testing expert.

Apply the MC/DC (Modified Condition/Decision Coverage) testing technique.

IMPORTANT RULES:
- Output ONLY raw JSON.
- Do NOT include explanations.
- Do NOT use markdown.
- Do NOT include backticks.
- Do NOT include any text before or after JSON.
- For normal cases, include the exact return value in `expected_return` and set `expected_exception` to null.
- For exception cases, set `expected_return` to null and `expected_exception` to the built-in exception class name.

Return JSON in exactly this format:

{{
  "function": "function_name",
  "decisions": [
    {{
      "decision": "boolean expression",
      "conditions": ["cond1", "cond2"],
      "test_cases": [
        {{
          "id": "TC1",
          "inputs": {{"parameter_name": "concrete argument value"}},
          "expected_behavior": "normal | exception",
          "expected_return": "exact return value or null",
          "expected_exception": "ValueError or null"
        }}
      ]
    }}
  ]
}}

Function under test:
-------------------
{function_code}
"""

STATE_BASED_PROMPT = """
You are a software testing expert.

Apply STATE-BASED TESTING to the Python class below.

IMPORTANT RULES:
- Output ONLY raw JSON.
- Do NOT include explanations.
- Do NOT use markdown.
- Do NOT include backticks.
- Focus on object states and transitions caused by method calls.
- Assume one fresh object instance is created per test case.
- Use the class attribute that stores the state in `state_attribute`.
- For each step, include the exact expected return value or exact expected exception class name.
- For each step, include the expected state after the action completes.

Return JSON in exactly this format:

{{
  "class_name": "ClassName",
  "state_attribute": "state",
  "states": ["state1", "state2"],
  "transitions": [
    {{
      "from": "state1",
      "action": "method_name",
      "to": "state2"
    }}
  ],
  "test_cases": [
    {{
      "id": "TC1",
      "description": "short explanation",
      "constructor_args": {{}},
      "expected_initial_state": "state1",
      "steps": [
        {{
          "action": "method_name",
          "args": {{}},
          "expected_behavior": "normal | exception",
          "expected_return": "exact return value or null",
          "expected_exception": "ValueError or null",
          "expected_state": "state after the action"
        }}
      ]
    }}
  ]
}}

Class under test:
-----------------
{function_code}
"""
