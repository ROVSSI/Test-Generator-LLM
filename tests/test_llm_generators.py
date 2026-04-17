import os
import sys
import json

ROOT_DIR = os.path.join(os.path.dirname(__file__), "..")
SRC_DIR = os.path.join(ROOT_DIR, "src")

sys.path.append(SRC_DIR)

from llm_json_utils import extract_json
from llm_mcdc_generator import generate_pytest_from_mcdc
from llm_test_generator import generate_pytest_from_cp
import testgen
from testgen import main


def test_extract_json_ignores_wrapping_text():
    parsed = extract_json('prefix {"first": 1} suffix {"second": 2}')
    assert parsed == {"first": 1}


def test_generate_pytest_from_cp_uses_keyword_args_and_exact_assertions():
    json_text = """
    {
      "function": "authorize",
      "parameters": {
        "user_role": {"categories": {"role": ["admin", "user"]}},
        "is_active": {"categories": {"state": [true, false]}},
        "has_2fa": {"categories": {"state": [true, false]}}
      },
      "invalid_combinations": [],
      "test_cases": [
        {
          "id": "TC1",
          "description": "active user with 2fa",
          "inputs": {
            "user_role": "user",
            "is_active": true,
            "has_2fa": true
          },
          "expected_behavior": "normal",
          "expected_return": true,
          "expected_exception": null
        }
      ]
    }
    """

    output = generate_pytest_from_cp(json_text, "refund_policy_code.py")

    assert "target_module.authorize(user_role='user', is_active=True, has_2fa=True)" in output
    assert "assert result == True" in output


def test_generate_pytest_from_mcdc_makes_duplicate_ids_unique():
    json_text = """
    {
      "function": "authorize",
      "decisions": [
        {
          "decision": "is_active and has_2fa",
          "conditions": ["is_active", "has_2fa"],
          "test_cases": [
            {
              "id": "TC1",
              "inputs": {
                "user_role": "admin",
                "is_active": false,
                "has_2fa": false
              },
              "expected_behavior": "normal",
              "expected_return": true,
              "expected_exception": null
            },
            {
              "id": "TC1",
              "inputs": {
                "user_role": "user",
                "is_active": true,
                "has_2fa": true
              },
              "expected_behavior": "normal",
              "expected_return": true,
              "expected_exception": null
            }
          ]
        }
      ]
    }
    """

    output = generate_pytest_from_mcdc(json_text, "order_routing_code.py")

    assert "def test_authorize_tc1():" in output
    assert "def test_authorize_tc1_2():" in output


def test_main_returns_nonzero_for_missing_file(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        ["testgen.py", "llm", "--method", "mcdc", "does-not-exist.py"],
    )

    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "[ERROR] File not found: does-not-exist.py" in captured.err


def test_main_repairs_invalid_llm_expectations_before_writing_pytest(monkeypatch, capsys, tmp_path):
    llm_output = json.dumps(
        {
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
    )

    output_root = tmp_path / "project"
    output_root.mkdir()
    monkeypatch.setattr(testgen, "PROJECT_ROOT", str(output_root))
    monkeypatch.setattr(testgen, "call_llm", lambda prompt: llm_output)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "testgen.py",
            "llm",
            "--method",
            "mcdc",
            os.path.join(ROOT_DIR, "src", "order_routing_code.py"),
        ],
    )

    exit_code = main()
    captured = capsys.readouterr()
    output_path = output_root / "tests" / "test_llm_mcdc.py"
    generated = output_path.read_text(encoding="utf-8")

    assert exit_code == 0
    assert "1 repaired" in captured.out
    assert "assert result == 'manual_review'" in generated


def test_main_writes_repaired_state_based_pytest(monkeypatch, capsys, tmp_path):
    llm_output = json.dumps(
        {
            "class_name": "RefundCase",
            "state_attribute": "state",
            "states": ["draft", "submitted", "under_review", "approved", "rejected", "closed"],
            "transitions": [],
            "test_cases": [
                {
                    "id": "TC1",
                    "description": "bad submit expectation",
                    "constructor_args": {},
                    "expected_initial_state": "draft",
                    "steps": [
                        {
                            "action": "submit",
                            "args": {},
                            "expected_behavior": "normal",
                            "expected_return": "approved",
                            "expected_exception": None,
                            "expected_state": "approved",
                        }
                    ],
                }
            ],
        }
    )

    output_root = tmp_path / "project"
    output_root.mkdir()
    monkeypatch.setattr(testgen, "PROJECT_ROOT", str(output_root))
    monkeypatch.setattr(testgen, "call_llm", lambda prompt: llm_output)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "testgen.py",
            "llm",
            "--method",
            "state_based",
            os.path.join(ROOT_DIR, "src", "refund_case_code.py"),
        ],
    )

    exit_code = main()
    captured = capsys.readouterr()
    output_path = output_root / "tests" / "test_llm_state_based.py"
    generated = output_path.read_text(encoding="utf-8")

    assert exit_code == 0
    assert "1 repaired" in captured.out
    assert "assert result == 'submitted'" in generated
    assert "assert obj.state == 'submitted'" in generated
