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
            "expected_behavior": "normal | exception",
            "expected_return": "exact return value or null",
            "expected_exception": "ValueError or null"
        }
    ]
}

MCDC_SCHEMA = {
    "function": "function_name",
    "decisions": [
        {
            "decision": "boolean expression",
            "conditions": ["cond1", "cond2"],
            "test_cases": [
                {
                    "id": "TC1",
                    "inputs": {
                        "param_name": "concrete input value"
                    },
                    "expected_behavior": "normal | exception",
                    "expected_return": "exact return value or null",
                    "expected_exception": "ValueError or null"
                }
            ]
        }
    ]
}

STATE_BASED_SCHEMA = {
    "class_name": "ClassName",
    "state_attribute": "state",
    "states": ["state1", "state2"],
    "transitions": [
        {
            "from": "state1",
            "action": "method_name",
            "to": "state2"
        }
    ],
    "test_cases": [
        {
            "id": "TC1",
            "description": "what sequence this test checks",
            "constructor_args": {},
            "expected_initial_state": "state1",
            "steps": [
                {
                    "action": "method_name",
                    "args": {},
                    "expected_behavior": "normal | exception",
                    "expected_return": "exact return value or null",
                    "expected_exception": "ValueError or null",
                    "expected_state": "state after the action"
                }
            ]
        }
    ]
}
