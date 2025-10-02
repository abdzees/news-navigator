"""
Embeddings module placeholder.

Implement an embeddings class that wraps SentenceTransformers to compute
article embeddings and persist/load them as needed.
"""


class EmbeddingModel:
    """Placeholder for embedding model wrapper."""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        # TODO: load SentenceTransformer model
        self.model = None

    def encode(self, texts):
        """Encode texts into vectors. Return list of vectors."""
        # TODO: implement model.encode(texts)
        return []
