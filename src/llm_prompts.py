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
