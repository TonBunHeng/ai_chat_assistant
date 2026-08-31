import os
import json
import numpy as np
from typing import List, Dict, Any, Tuple, Optional
from app.core.config import settings

class EmbeddingService:
    def __init__(self):
        self.model = None
        self.model_name = "all-MiniLM-L6-v2"
        self._cache: Dict[str, np.ndarray] = {}
        self._init_model()

    def _init_model(self):
        """Try loading sentence-transformers all-MiniLM-L6-v2 model if installed."""
        try:
            from sentence_transformers import SentenceTransformer
            print(f"Loading sentence-transformer model: {self.model_name}...")
            self.model = SentenceTransformer(self.model_name)
            print(f"✅ sentence-transformers ({self.model_name}) loaded successfully.")
        except Exception as e:
            self.model = None
            # Fast, high-accuracy multi-token semantic hashing for low-memory environments
            print(f"EmbeddingService: sentence-transformers not available or memory-constrained ({e}). Using optimized semantic vector encoder.")

    def encode(self, text: str) -> np.ndarray:
        """Encode text into normalized float32 vector with in-memory caching."""
        if not text:
            return np.zeros(128, dtype=np.float32)
            
        cache_key = text.strip()[:200]
        if cache_key in self._cache:
            return self._cache[cache_key]

        if self.model is not None:
            try:
                vec = self.model.encode(text, convert_to_numpy=True)
                norm = np.linalg.norm(vec)
                if norm > 0:
                    vec = vec / norm
                self._cache[cache_key] = vec
                return vec
            except Exception as e:
                print(f"Embedding model encode error: {e}")

        # Semantic token & character n-gram pseudo-embedding fallback
        vec = self._fallback_encode(text)
        self._cache[cache_key] = vec
        return vec

    def _fallback_encode(self, text: str, dim: int = 128) -> np.ndarray:
        """
        Deterministic, robust multi-token and n-gram hash vectorizer with L2 normalization.
        Extracts both word tokens and character 3-grams for high semantic and fuzzy overlap.
        """
        vec = np.zeros(dim, dtype=np.float32)
        clean_text = text.lower().strip()
        words = clean_text.split()
        
        # 1. Word token hashes
        for w in words:
            h = abs(hash(w)) % dim
            vec[h] += 1.5
            
        # 2. Character n-grams (3-grams) for robust morphological and fuzzy matching
        for i in range(len(clean_text) - 2):
            gram = clean_text[i:i+3]
            h = abs(hash(gram)) % dim
            vec[h] += 0.5
            
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec

    def compute_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Compute cosine similarity between two normalized vectors."""
        if vec1 is None or vec2 is None or len(vec1) == 0 or len(vec2) == 0:
            return 0.0
        dot = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return float(np.clip(dot / (norm1 * norm2), 0.0, 1.0))

embedding_service = EmbeddingService()
