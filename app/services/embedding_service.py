from functools import lru_cache

from sentence_transformers import SentenceTransformer

from app.core.config import settings

@lru_cache
def get_embedding_model() -> SentenceTransformer:
    return SentenceTransformer(settings.embedding_model)

def generate_embedding(text: str) -> list[float]:
    model = get_embedding_model()
    embedding = model.encode(text)

    return embedding.tolist()

def generate_embeddings(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []

    model = get_embedding_model()
    embeddings = model.encode(texts)

    return embeddings.tolist()