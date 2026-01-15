from openai import OpenAI
from .base import EmbeddingBackend
from ..config import Settings

client = OpenAI(api_key=Settings.OPENAI_API_KEY)

class OpenAIEmbeddingBackend(EmbeddingBackend):
    def __init__(self):
        self.client = client

    def embed(self, texts: list[str]):
        response = self.client.embeddings.create(
            input=texts,
            model="text-embedding-3-small"
        )
        return [data.embedding for data in response.data]
    