from openai import OpenAI
import os


def call_llm(prompt: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    content = response.choices[0].message.content
    if content is None:
        raise ValueError("LLM response did not contain message content")

    return content
