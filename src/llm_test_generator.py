from llm_json_utils import extract_json
from llm_codegen_utils import append_test_body, build_call_arguments, build_module_loader_lines, build_test_name

def generate_pytest_from_cp(json_text: str, source_file: str) -> str:
    return render_pytest_from_cp(extract_json(json_text), source_file)


def render_pytest_from_cp(data: dict, source_file: str) -> str:
    function_name = data["function"]
    lines = build_module_loader_lines(source_file)
    seen_names: dict[str, int] = {}

    for tc in data["test_cases"]:
        test_name = build_test_name(function_name, tc["id"], seen_names)
        lines.append(f"def {test_name}():")
        call_arguments = build_call_arguments(tc["inputs"])
        append_test_body(lines, function_name, call_arguments, tc)
        lines.append("")

    return "\n".join(lines)
