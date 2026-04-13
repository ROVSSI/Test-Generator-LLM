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
    if "class_name" in validated_spec:
        return _validate_state_spec(validated_spec, source_path)

    function_name = validated_spec["function"]
    target_function = load_target_member(source_path, function_name)
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


def load_target_member(source_path: str, member_name: str):
    spec = importlib.util.spec_from_file_location("validation_target_module", source_path)
    if spec is None or spec.loader is None:
        raise ValueError(f"Could not load source module from {source_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    target = getattr(module, member_name, None)
    if target is None or not callable(target):
        raise ValueError(f"Target {member_name!r} not found in {source_path}")

    return target


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
    custom_message = test_case.get("_validation_repair_message")
    if custom_message:
        return custom_message

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


def _validate_state_spec(spec: dict[str, Any], source_path: str) -> tuple[dict[str, Any], ValidationSummary]:
    validated_spec = deepcopy(spec)
    class_name = validated_spec["class_name"]
    target_class = load_target_member(source_path, class_name)
    state_attribute = validated_spec.get("state_attribute", "state")
    summary = ValidationSummary()

    for test_case in validated_spec["test_cases"]:
        summary.total_cases += 1

        if _repair_state_test_case(test_case, target_class, state_attribute):
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


def _repair_state_test_case(test_case: dict[str, Any], target_class, state_attribute: str) -> bool:
    constructor_args = test_case.get("constructor_args", {})
    if not isinstance(constructor_args, dict):
        raise ValueError(
            f"State-based test case {test_case.get('id', '<unknown>')!r} must define 'constructor_args' as an object."
        )

    instance = target_class(**constructor_args)
    repair_messages: list[str] = []

    actual_initial_state = getattr(instance, state_attribute)
    previous_initial_state = test_case.get("expected_initial_state")
    test_case["expected_initial_state"] = actual_initial_state
    if previous_initial_state != actual_initial_state:
        repair_messages.append(f"initial state {previous_initial_state!r} -> {actual_initial_state!r}")

    for step in test_case["steps"]:
        step_repairs = _repair_state_step(step, instance, state_attribute)
        repair_messages.extend(step_repairs)

    if repair_messages:
        test_case["_validation_repair_message"] = "; ".join(repair_messages)
        return True

    return False


def _repair_state_step(step: dict[str, Any], instance, state_attribute: str) -> list[str]:
    action_name = step.get("action")
    if not isinstance(action_name, str) or not action_name:
        raise ValueError("Each state-based step must define a non-empty 'action'.")

    step_args = step.get("args", {})
    if not isinstance(step_args, dict):
        raise ValueError(f"State-based action {action_name!r} must define 'args' as an object.")

    target_method = getattr(instance, action_name, None)
    if target_method is None or not callable(target_method):
        raise ValueError(f"Action {action_name!r} is not a callable method on {type(instance).__name__}.")

    previous_behavior = step.get("expected_behavior")
    previous_return = step.get("expected_return")
    previous_exception = step.get("expected_exception")
    previous_state = step.get("expected_state")

    try:
        result = target_method(**step_args)
    except Exception as exc:  # noqa: BLE001
        actual_behavior = "exception"
        actual_return = None
        actual_exception = type(exc).__name__
    else:
        actual_behavior = "normal"
        actual_return = result
        actual_exception = None

    actual_state = getattr(instance, state_attribute)
    step["expected_behavior"] = actual_behavior
    step["expected_return"] = actual_return
    step["expected_exception"] = actual_exception
    step["expected_state"] = actual_state

    repairs: list[str] = []
    if previous_behavior != actual_behavior or previous_return != actual_return or previous_exception != actual_exception:
        if actual_behavior == "exception":
            repairs.append(
                f"step {action_name!r} expected {previous_behavior}/{previous_exception!r} but raised {actual_exception!r}"
            )
        else:
            repairs.append(
                f"step {action_name!r} expected {previous_behavior}/{previous_return!r} but returned {actual_return!r}"
            )

    if previous_state != actual_state:
        repairs.append(f"step {action_name!r} state {previous_state!r} -> {actual_state!r}")

    return repairs
