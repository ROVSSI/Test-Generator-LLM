#!/usr/bin/env python3
import argparse
import os
import sys

# Allow imports from src/
PROJECT_ROOT = os.path.dirname(__file__)
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
sys.path.append(SRC_DIR)

from llm_client import call_llm
from llm_prompts import CATEGORY_PARTITION_PROMPT
from llm_test_generator import generate_pytest_from_cp


def cmd_llm_category_partition(filepath: str):
    if not os.path.exists(filepath):
        print(f"[ERROR] File not found: {filepath}")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        function_code = f.read()

    print("[INFO] Calling LLM with Category Partition prompt...")
    prompt = CATEGORY_PARTITION_PROMPT.format(function_code=function_code)

    llm_output = call_llm(prompt)



    print("[INFO] LLM responded. Generating pytest file...")

    # TEMPORARY: assume single function name (we'll generalize later)
    function_name = os.path.splitext(os.path.basename(filepath))[0]

    source_file = os.path.basename(filepath)
    test_code = generate_pytest_from_cp(llm_output, source_file)

    tests_dir = os.path.join(PROJECT_ROOT, "tests")
    os.makedirs(tests_dir, exist_ok=True)

    out_path = os.path.join(tests_dir, "test_llm_category_partition.py")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(test_code)

    print(f"[OK] LLM-based tests written to {out_path}")
    print("Run them with:")
    print("  pytest -v tests/test_llm_category_partition.py")




def main():
    parser = argparse.ArgumentParser(
        description="LLM-Guided Test Generator"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    llm_parser = sub.add_parser("llm", help="LLM-based test generation")
    llm_parser.add_argument(
        "--method",
        choices=["category_partition"],
        required=True
    )
    llm_parser.add_argument(
        "filepath",
        help="Python file containing the function under test"
    )

    args = parser.parse_args()

    if args.command == "llm":
        if args.method == "category_partition":
            cmd_llm_category_partition(args.filepath)


if __name__ == "__main__":
    main()
