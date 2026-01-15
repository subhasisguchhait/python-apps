import openai
import time
from config import settings 

openai.api_key = settings.OPENAI_API_KEY

def llm_run_evaluation(system_prompt: str, user_prompt: str, model: str) -> dict:

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt }
    ]

    start = time.time()
    # Call the OpenAI API to get the response
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.5
    )
    end = time.time()

    latency = f"{end - start:.2f} seconds"
    response_text = response.choices[0].message.content
    token = response.usage.total_tokens

    result = {
        "response": response_text,
        "latency": latency,
        "total_tokens": token
    }

    return result