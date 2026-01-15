from openai import OpenAI
from .config import Settings   

client = OpenAI(api_key=Settings.OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are a helpful assistant.
Answer ONLY using the provided context.
If the answer is not in the context, say "I don't know".
"""

def generate_answer(question: str, context_chunks: list[str]):
    # Combine context chunks into a single string
    context = "\n".join(context_chunks)

    # Create the prompt
    prompt = f"{SYSTEM_PROMPT}\n\nContext:\n{context}\n\nQuestion: {question}\nAnswer:"

    # Call OpenAI API to generate the answer
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0
    )

    answer = response.choices[0].message.content.strip()
    return answer