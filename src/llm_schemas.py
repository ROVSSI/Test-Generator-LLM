CATEGORY_PARTITION_SCHEMA = {
    "function": "string",
    "parameters": {
        "param_name": {
            "categories": {
                "category_name": ["choice1", "choice2"]
            }
        }
    },
    "invalid_combinations": [
        "description of invalid combination"
    ],
    "test_cases": [
        {
            "id": "TC1",
            "description": "what this test checks",
            "inputs": {
                "param_name": "choice"
            },
            "expected_behavior": "normal | exception"
        }
    ]
}