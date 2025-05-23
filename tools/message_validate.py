from openai import OpenAI


def test_message(messgage: str):
    client = OpenAI(api_key="c80d92cf-e029-4240-acd1-dd89b92f5137")
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
