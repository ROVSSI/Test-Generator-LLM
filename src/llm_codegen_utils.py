import re
from typing import Any


def build_module_loader_lines(source_file: str) -> list[str]:
    return [
        "import pytest",
        "import os, importlib.util",
        "",
        "BASE_DIR = os.path.dirname(__file__)",
        f"TARGET_PATH = os.path.join(BASE_DIR, '..', 'src', '{source_file}')",
        "spec = importlib.util.spec_from_file_location('target_module', TARGET_PATH)",
        "target_module = importlib.util.module_from_spec(spec)",
        "spec.loader.exec_module(target_module)",
        "",
    ]


def build_call_arguments(inputs: dict[str, Any]) -> str:
    if not isinstance(inputs, dict) or not inputs:
        raise ValueError("Each test case must define a non-empty 'inputs' object.")

    return ", ".join(f"{name}={value!r}" for name, value in inputs.items())


def build_test_name(function_name: str, case_id: str, seen_names: dict[str, int]) -> str:
    base_name = f"test_{_sanitize_identifier(function_name)}_{_sanitize_identifier(case_id)}"
    occurrence = seen_names.get(base_name, 0) + 1
    seen_names[base_name] = occurrence

    if occurrence == 1:
        return base_name

    return f"{base_name}_{occurrence}"


def append_test_body(lines: list[str], function_name: str, call_arguments: str, test_case: dict[str, Any]) -> None:
    expected_behavior = test_case.get("expected_behavior")

    if expected_behavior == "exception":
        exception_name = test_case.get("expected_exception") or "Exception"
        lines.append(f"    with pytest.raises({exception_name}):")
        lines.append(f"        target_module.{function_name}({call_arguments})")
        return

    if expected_behavior != "normal":
        raise ValueError(
            f"Unsupported expected_behavior {expected_behavior!r} for test case {test_case.get('id', '<unknown>')!r}."
        )

    if "expected_return" not in test_case:
        raise ValueError(
            f"Normal test case {test_case.get('id', '<unknown>')!r} is missing 'expected_return'."
        )

    lines.append(f"    result = target_module.{function_name}({call_arguments})")
    lines.append(f"    assert result == {test_case['expected_return']!r}")


def _sanitize_identifier(value: str) -> str:
    sanitized = re.sub(r"\W|^(?=\d)", "_", str(value).strip().lower())
    return sanitized or "generated"
