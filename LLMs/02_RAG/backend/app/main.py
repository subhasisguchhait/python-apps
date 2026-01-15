import os
from fastapi import FastAPI
from .rag import generate_answer

# # OPTION 1: Local embeddings (free)
# from app.embeddings.sentence_transformer import SentenceTransformerEmbedding
# embedder = SentenceTransformerEmbedding()

# OPTION 2: OpenAI embeddings (higher quality)
from .embeddings.openai_embedding import OpenAIEmbeddingBackend
embedder = OpenAIEmbeddingBackend()


from .chunker import chunk_text
from .vector_store import VectorStore

app = FastAPI()

# Load document
document_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'knowledge.txt'))
with open(document_path) as f:
    raw_text = f.read()

# Chunk document
chunks = chunk_text(raw_text)

# Create embeddings for chunks
embeddings = embedder.embed(chunks)

# Initialize vector store
vector_store = VectorStore(dim=len(embeddings[0]))
# Add embeddings and chunks to vector store
vector_store.add(embeddings, chunks)

@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/ask")
def ask(request: dict):
    # Embed user question
    question = request["user_prompt"]
    question_embedding = embedder.embed([question])[0]

    # Retrieve relevant chunks
    relevant_chunks = vector_store.search(question_embedding)

    # Generate grounded answer using LLM
    answer = generate_answer(question, relevant_chunks)

    return {
        "answer": answer,
        "sources": relevant_chunks
    }


# @app.post("/ask_v2")
# def ask_v2(x: dict):
#     question = x["user_prompt"]
#     return {"answer": f"You asked: {question}"}
    