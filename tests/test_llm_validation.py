import os
import sys

ROOT_DIR = os.path.join(os.path.dirname(__file__), "..")
SRC_DIR = os.path.join(ROOT_DIR, "src")

sys.path.append(SRC_DIR)

from llm_validation import format_validation_summary, validate_test_spec


def test_validate_test_spec_repairs_wrong_normal_oracle():
    spec = {
        "function": "route_order",
        "decisions": [
            {
                "decision": "manual review boundary",
                "conditions": ["destination == 'domestic'", "order_total < 20"],
                "test_cases": [
                    {
                        "id": "TC2",
                        "inputs": {
                            "order_total": 0,
                            "customer_tier": "standard",
                            "is_express": False,
                            "has_coupon": False,
                            "destination": "domestic",
                        },
                        "expected_behavior": "normal",
                        "expected_return": "standard",
                        "expected_exception": None,
                    }
                ],
            }
        ],
    }

    validated_spec, summary = validate_test_spec(spec, os.path.join(ROOT_DIR, "src", "order_routing_code.py"))
    test_case = validated_spec["decisions"][0]["test_cases"][0]

    assert test_case["expected_behavior"] == "normal"
    assert test_case["expected_return"] == "manual_review"
    assert test_case["expected_exception"] is None
    assert summary.confirmed_cases == 0
    assert summary.repaired_cases == 1


def test_validate_test_spec_repairs_normal_case_into_exception_case():
    spec = {
        "function": "route_order",
        "test_cases": [
            {
                "id": "TC1",
                "inputs": {
                    "order_total": -1,
                    "customer_tier": "standard",
                    "is_express": False,
                    "has_coupon": False,
                    "destination": "domestic",
                },
                "expected_behavior": "normal",
                "expected_return": "standard",
                "expected_exception": None,
            }
        ],
    }

    validated_spec, summary = validate_test_spec(spec, os.path.join(ROOT_DIR, "src", "order_routing_code.py"))
    test_case = validated_spec["test_cases"][0]

    assert test_case["expected_behavior"] == "exception"
    assert test_case["expected_return"] is None
    assert test_case["expected_exception"] == "ValueError"
    assert summary.repaired_cases == 1


def test_format_validation_summary_lists_repairs():
    spec = {
        "function": "route_order",
        "test_cases": [
            {
                "id": "TC15",
                "inputs": {
                    "order_total": 70,
                    "customer_tier": "standard",
                    "is_express": False,
                    "has_coupon": True,
                    "destination": "domestic",
                },
                "expected_behavior": "normal",
                "expected_return": "discount_only",
                "expected_exception": None,
            }
        ],
    }

    _, summary = validate_test_spec(spec, os.path.join(ROOT_DIR, "src", "order_routing_code.py"))
    lines = format_validation_summary(summary)

    assert "1 repaired" in lines[0]
    assert any("TC15" in line and "standard" in line for line in lines[1:])
