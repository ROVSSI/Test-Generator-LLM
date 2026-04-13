from llm_json_utils import extract_json
from llm_codegen_utils import (
    build_call_arguments,
    build_exception_reference,
    build_module_loader_lines,
    build_test_name,
)


def generate_pytest_from_state(json_text: str, source_file: str) -> str:
    return render_pytest_from_state(extract_json(json_text), source_file)


def render_pytest_from_state(data: dict, source_file: str) -> str:
    class_name = data["class_name"]
    state_attribute = data.get("state_attribute", "state")
    lines = build_module_loader_lines(source_file)
    seen_names: dict[str, int] = {}

    for test_case in data["test_cases"]:
        test_name = build_test_name(class_name, test_case["id"], seen_names)
        lines.append(f"def {test_name}():")

        constructor_args = build_call_arguments(test_case.get("constructor_args", {}), allow_empty=True)
        if constructor_args:
            lines.append(f"    obj = target_module.{class_name}({constructor_args})")
        else:
            lines.append(f"    obj = target_module.{class_name}()")

        if "expected_initial_state" in test_case:
            lines.append(f"    assert obj.{state_attribute} == {test_case['expected_initial_state']!r}")

        for step in test_case["steps"]:
            step_args = build_call_arguments(step.get("args", {}), allow_empty=True)
            step_call = f"obj.{step['action']}({step_args})" if step_args else f"obj.{step['action']}()"

            if step["expected_behavior"] == "exception":
                exception_name = step.get("expected_exception") or "Exception"
                lines.append(f"    with pytest.raises({build_exception_reference(exception_name)}):")
                lines.append(f"        {step_call}")
            else:
                lines.append(f"    result = {step_call}")
                lines.append(f"    assert result == {step['expected_return']!r}")

            lines.append(f"    assert obj.{state_attribute} == {step['expected_state']!r}")

        lines.append("")

    return "\n".join(lines)
