from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
import importlib.util
from typing import Any


@dataclass
class ValidationRepair:
    case_id: str
    message: str


@dataclass
class ValidationSummary:
    total_cases: int = 0
    confirmed_cases: int = 0
    repaired_cases: int = 0
    repairs: list[ValidationRepair] = field(default_factory=list)


def validate_test_spec(spec: dict[str, Any], source_path: str) -> tuple[dict[str, Any], ValidationSummary]:
    validated_spec = deepcopy(spec)
    function_name = validated_spec["function"]
    target_function = load_target_function(source_path, function_name)
    summary = ValidationSummary()

    for test_case in iter_test_cases(validated_spec):
        summary.total_cases += 1

        if _repair_test_case(test_case, target_function):
            summary.repaired_cases += 1
            summary.repairs.append(
                ValidationRepair(
                    case_id=str(test_case.get("id", "<unknown>")),
                    message=build_repair_message(test_case),
                )
            )
        else:
            summary.confirmed_cases += 1

    return validated_spec, summary


def format_validation_summary(summary: ValidationSummary) -> list[str]:
    lines = [
        "[INFO] Validation summary: "
        f"{summary.confirmed_cases} confirmed, {summary.repaired_cases} repaired, {summary.total_cases} total."
    ]

    for repair in summary.repairs:
        lines.append(f"[INFO] Repaired {repair.case_id}: {repair.message}")

    return lines


def iter_test_cases(spec: dict[str, Any]):
    if "test_cases" in spec:
        yield from spec["test_cases"]
        return

    for decision in spec.get("decisions", []):
        yield from decision.get("test_cases", [])


def load_target_function(source_path: str, function_name: str):
    spec = importlib.util.spec_from_file_location("validation_target_module", source_path)
    if spec is None or spec.loader is None:
        raise ValueError(f"Could not load source module from {source_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    target_function = getattr(module, function_name, None)
    if target_function is None or not callable(target_function):
        raise ValueError(f"Function {function_name!r} not found in {source_path}")

    return target_function


def _repair_test_case(test_case: dict[str, Any], target_function) -> bool:
    inputs = test_case.get("inputs")
    if not isinstance(inputs, dict) or not inputs:
        raise ValueError(f"Test case {test_case.get('id', '<unknown>')!r} must define a non-empty 'inputs' object.")

    previous_behavior = test_case.get("expected_behavior")
    previous_return = test_case.get("expected_return")
    previous_exception = test_case.get("expected_exception")

    try:
        result = target_function(**inputs)
    except Exception as exc:  # noqa: BLE001
        actual_behavior = "exception"
        actual_return = None
        actual_exception = type(exc).__name__
    else:
        actual_behavior = "normal"
        actual_return = result
        actual_exception = None

    test_case["expected_behavior"] = actual_behavior
    test_case["expected_return"] = actual_return
    test_case["expected_exception"] = actual_exception
    test_case["_validation_previous"] = {
        "expected_behavior": previous_behavior,
        "expected_return": previous_return,
        "expected_exception": previous_exception,
    }

    return (
        previous_behavior != actual_behavior
        or previous_return != actual_return
        or previous_exception != actual_exception
    )


def build_repair_message(test_case: dict[str, Any]) -> str:
    previous = test_case.get("_validation_previous", {})
    previous_behavior = previous.get("expected_behavior")
    previous_return = previous.get("expected_return")
    previous_exception = previous.get("expected_exception")
    actual_behavior = test_case.get("expected_behavior")
    actual_return = test_case.get("expected_return")
    actual_exception = test_case.get("expected_exception")

    if actual_behavior == "exception":
        return (
            "expected "
            f"{previous_behavior}/{previous_exception!r} "
            f"but execution raised {actual_exception!r}."
        )

    return (
        "expected "
        f"{previous_behavior}/{previous_return!r} "
        f"but execution returned {actual_return!r}."
    )
