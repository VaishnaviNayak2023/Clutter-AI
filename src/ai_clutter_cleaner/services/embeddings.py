"""Semantic embedding service."""


import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from src.ai_clutter_cleaner.config import DEFAULT_EMBEDDING_MODEL
from src.ai_clutter_cleaner.models import SimilarityMatch


class SemanticFinder:
    """Find semantically similar documents using embeddings."""

    def __init__(self, model_name: str = DEFAULT_EMBEDDING_MODEL):
        """
        Initialize the semantic finder.

        Args:
            model_name: Name of the Sentence Transformer model to use
        """
        self.model_name = model_name
        self.model = None
        self._is_loaded = False

    def load_model(self) -> None:
        """Load the embedding model (lazy loading)."""
        if not self._is_loaded:
            self.model = SentenceTransformer(self.model_name)
            self._is_loaded = True

    def find_similar(
        self,
        texts: list[str],
        threshold: float = 0.80,
        indices: list[int] | None = None,
    ) -> list[SimilarityMatch]:
        """
        Find semantically similar documents.

        Args:
            texts: List of document texts
            threshold: Similarity threshold (0.0 to 1.0)
            indices: Optional list of indices to use (for processing subsets)

        Returns:
            List of SimilarityMatch objects
        """
        if len(texts) < 2:
            return []

        # Load model if not already loaded
        self.load_model()

        # Use provided indices or all indices
        if indices is None:
            indices = list(range(len(texts)))

        # Filter to only process documents with sufficient text
        valid_indices = [i for i in indices if i < len(texts) and len(texts[i]) > 10]

        if len(valid_indices) < 2:
            return []

        # Generate embeddings
        valid_texts = [texts[i] for i in valid_indices]
        vectors = self.model.encode(
            valid_texts, normalize_embeddings=True, show_progress_bar=False
        )

        # Compute similarity matrix
        similarity_matrix = cosine_similarity(vectors)

        # Find pairs above threshold
        matches = []
        for i in range(len(valid_indices)):
            for j in range(i + 1, len(valid_indices)):
                score = float(similarity_matrix[i, j])
                if score >= threshold:
                    matches.append(
                        SimilarityMatch(
                            file_id_a=valid_indices[i],
                            file_id_b=valid_indices[j],
                            similarity_score=round(score, 4),
                            comparison_method=f"semantic-{self.model_name}",
                        )
                    )

        # Sort by similarity score (highest first)
        matches.sort(key=lambda x: x.similarity_score, reverse=True)

        return matches

    def compute_embeddings(self, texts: list[str]) -> np.ndarray:
        """
        Compute embeddings for a list of texts.

        Args:
            texts: List of document texts

        Returns:
            NumPy array of embeddings
        """
        self.load_model()
        return self.model.encode(texts, normalize_embeddings=True, show_progress_bar=False)


# Global finder instance
_finder_instance: SemanticFinder | None = None


def get_semantic_finder() -> SemanticFinder:
    """Get or create the global semantic finder instance."""
    global _finder_instance
    if _finder_instance is None:
        _finder_instance = SemanticFinder()
    return _finder_instance


def find_similar_documents(
    texts: list[str], threshold: float = 0.80
) -> list[SimilarityMatch]:
    """
    Find semantically similar documents.

    Args:
        texts: List of document texts
        threshold: Similarity threshold

    Returns:
        List of SimilarityMatch objects
    """
    finder = get_semantic_finder()
    return finder.find_similar(texts, threshold)
