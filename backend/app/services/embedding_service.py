import os
import json
import numpy as np
from typing import List, Dict, Any, Tuple
from app.core.config import settings

class EmbeddingService:
    def __init__(self):
        self.model = None
        self.vector_cache_path = os.path.join(settings.VECTOR_DB_DIR, "index_cache.json")
        os.makedirs(settings.VECTOR_DB_DIR, exist_ok=True)
        self._init_model()

    def _init_model(self):
        """Attempt to load sentence-transformers model; fallback to lightweight vector model."""
        try:
            # pyrefly: ignore [missing-import]
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            print("Loaded SentenceTransformer model: all-MiniLM-L6-v2")
        except Exception as e:
            print(f"SentenceTransformer not available ({e}). Using lightweight vector encoder.")
            self.model = None

    def encode(self, text: str) -> np.ndarray:
        """Encode text to vector array."""
        if self.model is not None:
            return self.model.encode(text, convert_to_numpy=True)
        else:
            # Simple TF-IDF / character n-gram pseudo-embedding fallback
            return self._fallback_encode(text)

    def _fallback_encode(self, text: str, dim: int = 128) -> np.ndarray:
        """Lightweight character/token hash embedding generator."""
        vec = np.zeros(dim, dtype=np.float32)
        words = text.lower().split()
        for w in words:
            h = hash(w) % dim
            vec[h] += 1.0
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec

    def compute_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Compute cosine similarity between two vectors."""
        dot = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return float(dot / (norm1 * norm2))

embedding_service = EmbeddingService()
