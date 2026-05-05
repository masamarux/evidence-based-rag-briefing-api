from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Chunk, Source
from app.services.embedding_service import generate_embedding


def retrieve_relevant_chunks(
    db: Session,
    case_id,
    question: str,
    top_k: int = 5,
):
    question_embedding = generate_embedding(question)

    distance = Chunk.embedding.cosine_distance(question_embedding)

    statement = (
        select(
            Chunk,
            Source.title.label("source_title"),
            distance.label("distance"),
        )
        .join(Source, Chunk.source_id == Source.id)
        .where(Source.case_id == case_id)
        .order_by(distance)
        .limit(top_k)
    )

    results = db.execute(statement).all()

    return [
        {
            "chunk": chunk,
            "source_title": source_title,
            "distance": distance_value,
            "similarity_score": 1 - distance_value,
        }
        for chunk, source_title, distance_value in results
    ]


def build_context(retrieved_chunks: list[dict]) -> str:
    context_parts: list[str] = []

    for index, item in enumerate(retrieved_chunks, start=1):
        chunk = item["chunk"]
        source_title = item["source_title"]

        context_parts.append(
            f"[Evidence {index} | Source: {source_title}]\n{chunk.content}"
        )

    return "\n\n".join(context_parts)


def build_fallback_answer(question: str, retrieved_chunks: list[dict]) -> str:
    if not retrieved_chunks:
        return (
            "I could not find relevant evidence in the available sources "
            "to answer this question."
        )

    return (
        "I found relevant evidence in the case sources, but no LLM is configured yet. "
        "Review the evidence_used field to inspect the supporting context for this question."
    )