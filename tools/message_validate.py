import os
from openai import OpenAI


def test_message(messgage: str):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY_3"))
    try:
        client.chat.completions.create(
            model="Qwen/Qwen3-235B-A22B",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": messgage},
            ],
            extra_body={
                "enable_thinking": False,
            },
        )
        return True
    except Exception as e:
        print(e)
        return False
