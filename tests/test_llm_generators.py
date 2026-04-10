import os
import sys

ROOT_DIR = os.path.join(os.path.dirname(__file__), "..")
SRC_DIR = os.path.join(ROOT_DIR, "src")

sys.path.append(SRC_DIR)

from llm_json_utils import extract_json
from llm_mcdc_generator import generate_pytest_from_mcdc
from llm_test_generator import generate_pytest_from_cp
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

    output = generate_pytest_from_cp(json_text, "complex_code.py")

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

    output = generate_pytest_from_mcdc(json_text, "complex_code.py")

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
