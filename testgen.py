#!/usr/bin/env python3
import argparse
import os
import sys

# Allow imports from src/
PROJECT_ROOT = os.path.dirname(__file__)
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
sys.path.append(SRC_DIR)

from llm_client import call_llm
from llm_prompts import CATEGORY_PARTITION_PROMPT, MCDC_PROMPT
from llm_test_generator import generate_pytest_from_cp
from llm_mcdc_generator import generate_pytest_from_mcdc


def main():
    parser = argparse.ArgumentParser(
        description="LLM-Guided Test Generator"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    llm_parser = sub.add_parser("llm", help="LLM-based test generation")
    llm_parser.add_argument(
        "--method",
        choices=["category_partition", "mcdc"],
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
            print(f"[ERROR] File not found: {args.filepath}")
            return

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
            test_code = generate_pytest_from_cp(
                llm_output,
                source_file
            )
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
            test_code = generate_pytest_from_mcdc(
                llm_output,
                source_file
            )
            out_file = "test_llm_mcdc.py"

        # Write output
        tests_dir = os.path.join(PROJECT_ROOT, "tests")
        os.makedirs(tests_dir, exist_ok=True)

        out_path = os.path.join(tests_dir, out_file)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(test_code)

        print(f"[OK] LLM-based tests written to {out_path}")
        print(f"Run with: pytest -v tests/{out_file}")


if __name__ == "__main__":
    main()
