import faiss
import numpy as np

class VectorStore:
    def __init__(self, dim: int):
        # Create FAISS index using L2 distance
        self.index = faiss.IndexFlatL2(dim)
        self.texts = []

    def add(self, embeddings, texts):
        # Store embeddings in FAISS index
        self.index.add(np.array(embeddings).astype("float32"))
        self.texts.extend(texts)

    def search(self, query_embedding, k=3):
        # Search for top-k similar vectors
        distances, indices = self.index.search(
            np.array([query_embedding]).astype("float32"), k
        )
        return [self.texts[i] for i in indices[0]]
