#!/usr/bin/env python3
import argparse
import os
import sys

# Allow imports from src/
PROJECT_ROOT = os.path.dirname(__file__)
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
sys.path.append(SRC_DIR)

from llm_client import call_llm
from llm_prompts import CATEGORY_PARTITION_PROMPT, MCDC_PROMPT, STATE_BASED_PROMPT
from llm_json_utils import extract_json
from llm_mcdc_generator import render_pytest_from_mcdc
from llm_state_generator import render_pytest_from_state
from llm_test_generator import render_pytest_from_cp
from llm_validation import format_validation_summary, validate_test_spec


def main() -> int:
    parser = argparse.ArgumentParser(
        description="LLM-Guided Test Generator"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    llm_parser = sub.add_parser("llm", help="LLM-based test generation")
    llm_parser.add_argument(
        "--method",
        choices=["category_partition", "mcdc", "state_based"],
        required=True,
        help="Testing strategy to apply"
    )
    llm_parser.add_argument(
        "filepath",
        help="Python file containing the function under test"
    )

    args = parser.parse_args()

    if args.command == "llm":
        if not os.path.exists(args.filepath):
            print(f"[ERROR] File not found: {args.filepath}", file=sys.stderr)
            return 1

        try:
            # Read source code
            with open(args.filepath, "r", encoding="utf-8") as f:
                function_code = f.read()

            source_file = os.path.basename(args.filepath)

            # ------------------------------
            # CATEGORY PARTITION
            # ------------------------------
            if args.method == "category_partition":
                print("[INFO] Calling LLM with Category Partition prompt...")
                prompt = CATEGORY_PARTITION_PROMPT.format(
                    function_code=function_code
                )
                llm_output = call_llm(prompt)
                test_spec = extract_json(llm_output)
                validated_spec, validation_summary = validate_test_spec(test_spec, args.filepath)
                test_code = render_pytest_from_cp(validated_spec, source_file)
                out_file = "test_llm_category_partition.py"

            # ------------------------------
            # MC/DC
            # ------------------------------
            elif args.method == "mcdc":
                print("[INFO] Calling LLM with MC/DC prompt...")
                prompt = MCDC_PROMPT.format(
                    function_code=function_code
                )
                llm_output = call_llm(prompt)
                test_spec = extract_json(llm_output)
                validated_spec, validation_summary = validate_test_spec(test_spec, args.filepath)
                test_code = render_pytest_from_mcdc(validated_spec, source_file)
                out_file = "test_llm_mcdc.py"

            # ------------------------------
            # STATE-BASED TESTING
            # ------------------------------
            elif args.method == "state_based":
                print("[INFO] Calling LLM with State-Based Testing prompt...")
                prompt = STATE_BASED_PROMPT.format(
                    function_code=function_code
                )
                llm_output = call_llm(prompt)
                test_spec = extract_json(llm_output)
                validated_spec, validation_summary = validate_test_spec(test_spec, args.filepath)
                test_code = render_pytest_from_state(validated_spec, source_file)
                out_file = "test_llm_state_based.py"

            # Write output
            tests_dir = os.path.join(PROJECT_ROOT, "tests")
            os.makedirs(tests_dir, exist_ok=True)

            out_path = os.path.join(tests_dir, out_file)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(test_code)
        except Exception as exc:
            print(f"[ERROR] {exc}", file=sys.stderr)
            return 1

        for line in format_validation_summary(validation_summary):
            print(line)
        print(f"[OK] LLM-based tests written to {out_path}")
        print(f"Run with: pytest -v tests/{out_file}")
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
