"""
Embeddings wrapper using SentenceTransformers.

Provides:
- encode_article(text) -> vector (list[float] or numpy array)
- similarity(a, b) -> cosine similarity

Model loading is lazy and errors are handled gracefully so the app can run
without the heavy model when not needed.
"""
from typing import List, Optional, Union

import math


class EmbeddingModel:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        self._np = None

    def _ensure_model(self):
        if self.model is None:
            try:
                from sentence_transformers import SentenceTransformer
                import numpy as _np

                self.model = SentenceTransformer(self.model_name)
                self._np = _np
            except Exception:
                # If model import/loading fails, keep model as None. Callers should
                # check for None and fall back to non-embedding logic.
                self.model = None
                self._np = None

    def encode_article(self, text: str) -> Optional[object]:
        """Encode a single article text into an embedding vector.

        Returns a numpy array-like vector or None if the model couldn't be loaded.
        """
        if not text:
            return None
        self._ensure_model()
        if not self.model:
            return None
        vec = self.model.encode(text, convert_to_numpy=True)
        return vec

    def similarity(self, a: Union[List[float], object], b: Union[List[float], object]) -> Optional[float]:
        """Compute cosine similarity between two vectors (numpy arrays or lists).

        Returns None if vectors are missing or model numpy is unavailable.
        """
        if a is None or b is None:
            return None
        self._ensure_model()
        if not self._np:
            return None
        try:
            a_arr = self._np.array(a, dtype=float)
            b_arr = self._np.array(b, dtype=float)
            denom = (self._np.linalg.norm(a_arr) * self._np.linalg.norm(b_arr))
            if denom == 0:
                return 0.0
            return float(self._np.dot(a_arr, b_arr) / denom)
        except Exception:
            return None


# Module-level singleton
_default_embedding: Optional[EmbeddingModel] = None


def get_embedding_model(model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> EmbeddingModel:
    global _default_embedding
    if _default_embedding is None:
        _default_embedding = EmbeddingModel(model_name=model_name)
    return _default_embedding
