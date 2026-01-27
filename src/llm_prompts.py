CATEGORY_PARTITION_PROMPT = """
You are a software testing expert.

Apply the CATEGORY PARTITION testing technique.

Return ONLY valid JSON following this structure:
{{
  "function": "...",
  "parameters": {{
    "param": {{
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
      "inputs": {{"param": "choice"}},
      "expected_behavior": "normal | exception"
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
          "inputs": {{"param": [values]}},
          "expected_behavior": "normal"
        }}
      ]
    }}
  ]
}}

Function under test:
-------------------
{function_code}
"""
