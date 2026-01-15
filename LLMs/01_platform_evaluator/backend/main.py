from fastapi import FastAPI
from llms import llm_run_evaluation


app =FastAPI()

@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/run_evaluation")
def run_evaluation(request: dict):
    # Placeholder for the evaluation logic
    system_prompt = request.get("system_prompt")
    user_prompt = request.get("user_prompt")
    model = request.get("model")
    result = llm_run_evaluation(system_prompt, user_prompt, model)
    return result