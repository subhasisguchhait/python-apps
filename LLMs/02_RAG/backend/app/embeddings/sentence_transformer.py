from sentence_transformers import SentenceTransformer
from app.embeddings.base import EmbeddingBackend

class SentenceTransformerBackend(EmbeddingBackend):
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed(self, texts: list[str]):
        return self.model.encode(texts).tolist()
