import os
import sys
import json

ROOT_DIR = os.path.join(os.path.dirname(__file__), "..")
SRC_DIR = os.path.join(ROOT_DIR, "src")

sys.path.append(SRC_DIR)

from llm_state_generator import generate_pytest_from_state
from llm_validation import validate_test_spec


def test_generate_pytest_from_state_renders_method_sequence_and_state_assertions():
    json_text = """
    {
      "class_name": "Turnstile",
      "state_attribute": "state",
      "states": ["locked", "unlocked", "alarm"],
      "transitions": [],
      "test_cases": [
        {
          "id": "TC1",
          "description": "coin then push",
          "constructor_args": {},
          "expected_initial_state": "locked",
          "steps": [
            {
              "action": "insert_coin",
              "args": {},
              "expected_behavior": "normal",
              "expected_return": "unlocked",
              "expected_exception": null,
              "expected_state": "unlocked"
            },
            {
              "action": "push",
              "args": {},
              "expected_behavior": "normal",
              "expected_return": "passed",
              "expected_exception": null,
              "expected_state": "locked"
            }
          ]
        }
      ]
    }
    """

    output = generate_pytest_from_state(json_text, "turnstile_code.py")

    assert "obj = target_module.Turnstile()" in output
    assert "assert obj.state == 'locked'" in output
    assert "result = obj.insert_coin()" in output
    assert "assert result == 'unlocked'" in output
    assert "result = obj.push()" in output
    assert "assert obj.state == 'locked'" in output


def test_validate_test_spec_repairs_state_based_sequence():
    spec = {
        "class_name": "Turnstile",
        "state_attribute": "state",
        "states": ["locked", "unlocked", "alarm"],
        "transitions": [],
        "test_cases": [
            {
                "id": "TC2",
                "description": "wrong expectations",
                "constructor_args": {},
                "expected_initial_state": "unlocked",
                "steps": [
                    {
                        "action": "push",
                        "args": {},
                        "expected_behavior": "normal",
                        "expected_return": "passed",
                        "expected_exception": None,
                        "expected_state": "locked",
                    },
                    {
                        "action": "reset_alarm",
                        "args": {},
                        "expected_behavior": "normal",
                        "expected_return": "noop",
                        "expected_exception": None,
                        "expected_state": "alarm",
                    },
                ],
            }
        ],
    }

    validated_spec, summary = validate_test_spec(spec, os.path.join(ROOT_DIR, "src", "turnstile_code.py"))
    test_case = validated_spec["test_cases"][0]

    assert test_case["expected_initial_state"] == "locked"
    assert test_case["steps"][0]["expected_return"] == "alarm"
    assert test_case["steps"][0]["expected_state"] == "alarm"
    assert test_case["steps"][1]["expected_return"] == "reset"
    assert test_case["steps"][1]["expected_state"] == "locked"
    assert summary.repaired_cases == 1


def test_validate_test_spec_repairs_state_based_exception_step():
    spec = {
        "class_name": "Turnstile",
        "state_attribute": "state",
        "states": ["locked", "unlocked", "alarm"],
        "transitions": [],
        "test_cases": [
            {
                "id": "TC3",
                "description": "maintenance while unlocked",
                "constructor_args": {},
                "expected_initial_state": "locked",
                "steps": [
                    {
                        "action": "insert_coin",
                        "args": {},
                        "expected_behavior": "normal",
                        "expected_return": "unlocked",
                        "expected_exception": None,
                        "expected_state": "unlocked",
                    },
                    {
                        "action": "lock_for_maintenance",
                        "args": {},
                        "expected_behavior": "normal",
                        "expected_return": "locked",
                        "expected_exception": None,
                        "expected_state": "locked",
                    },
                ],
            }
        ],
    }

    validated_spec, summary = validate_test_spec(spec, os.path.join(ROOT_DIR, "src", "turnstile_code.py"))
    failing_step = validated_spec["test_cases"][0]["steps"][1]

    assert failing_step["expected_behavior"] == "exception"
    assert failing_step["expected_exception"] == "ValueError"
    assert failing_step["expected_state"] == "unlocked"
    assert summary.repaired_cases == 1
