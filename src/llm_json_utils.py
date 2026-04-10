import json

def extract_json(text: str) -> dict:
    """
    Extract first JSON object from LLM output.
    """
    decoder = json.JSONDecoder()

    for index, char in enumerate(text):
        if char != "{":
            continue

        try:
            parsed, _ = decoder.raw_decode(text[index:])
        except json.JSONDecodeError:
            continue

        if isinstance(parsed, dict):
            return parsed

    raise ValueError("No JSON object found in LLM output")
