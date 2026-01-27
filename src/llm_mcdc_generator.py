import json

from llm_json_utils import extract_json


def generate_pytest_from_mcdc(json_text: str, source_file: str) -> str:
    data = extract_json(json_text)
    function_name = data["function"]

    lines = []
    lines.append("import pytest")
    lines.append("import os, importlib.util")
    lines.append("")
    lines.append("BASE_DIR = os.path.dirname(__file__)")
    lines.append(
        f"TARGET_PATH = os.path.join(BASE_DIR, '..', 'src', '{source_file}')"
    )
    lines.append(
        "spec = importlib.util.spec_from_file_location('target_module', TARGET_PATH)"
    )
    lines.append("target_module = importlib.util.module_from_spec(spec)")
    lines.append("spec.loader.exec_module(target_module)")
    lines.append("")

    for decision in data["decisions"]:
        for tc in decision["test_cases"]:
            test_name = f"test_{function_name}_{tc['id'].lower()}"
            lines.append(f"def {test_name}():")
            args = ", ".join(repr(v) for v in tc["inputs"]["param"])

            if tc["expected_behavior"] == "exception":
                lines.append("    with pytest.raises(Exception):")
                lines.append(f"        target_module.{function_name}({args})")
            else:
                lines.append(f"    result = target_module.{function_name}({args})")
                lines.append("    assert result is not None")

            lines.append("")

    return "\n".join(lines)
