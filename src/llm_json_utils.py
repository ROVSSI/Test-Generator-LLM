import json

def extract_json(text: str) -> dict:
    """
    Robustly extract the first JSON object from LLM output.
    """
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise ValueError("No valid JSON object found in LLM output")

    json_str = text[start:end + 1]
    return json.loads(json_str)
