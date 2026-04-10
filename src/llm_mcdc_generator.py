from llm_json_utils import extract_json
from llm_codegen_utils import append_test_body, build_call_arguments, build_module_loader_lines, build_test_name


def generate_pytest_from_mcdc(json_text: str, source_file: str) -> str:
    data = extract_json(json_text)
    function_name = data["function"]

    lines = build_module_loader_lines(source_file)
    seen_names: dict[str, int] = {}

    for decision in data["decisions"]:
        for tc in decision["test_cases"]:
            test_name = build_test_name(function_name, tc["id"], seen_names)
            lines.append(f"def {test_name}():")
            call_arguments = build_call_arguments(tc["inputs"])
            append_test_body(lines, function_name, call_arguments, tc)
            lines.append("")

    return "\n".join(lines)
