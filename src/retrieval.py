from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievedChunk:
    source: str
    text: str
    score: float


def chunk_markdown(text: str, source: str) -> list[RetrievedChunk]:
    chunks: list[RetrievedChunk] = []
    for block in text.split("\n\n"):
        cleaned = " ".join(block.split())
        if cleaned:
            chunks.append(RetrievedChunk(source=source, text=cleaned, score=0.0))
    return chunks


class KeywordVectorIndex:
    """Tiny local retrieval layer that stands in for Foundry IQ semantic retrieval."""

    def __init__(self, chunks: list[RetrievedChunk]) -> None:
        self._chunks = chunks
        self._vectors = [_vectorize(chunk.text) for chunk in chunks]

    def search(self, query: str, top_k: int = 4) -> list[RetrievedChunk]:
        query_vector = _vectorize(query)
        scored: list[RetrievedChunk] = []

        for chunk, vector in zip(self._chunks, self._vectors, strict=True):
            score = _cosine_similarity(query_vector, vector)
            if score > 0:
                scored.append(RetrievedChunk(chunk.source, chunk.text, round(score, 4)))

        return sorted(scored, key=lambda item: item.score, reverse=True)[:top_k]


def _vectorize(text: str) -> Counter[str]:
    words = re.findall(r"[a-zA-Z0-9-]+", text.lower())
    return Counter(word for word in words if len(word) > 2)


def _cosine_similarity(left: Counter[str], right: Counter[str]) -> float:
    common_terms = set(left) & set(right)
    numerator = sum(left[term] * right[term] for term in common_terms)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))

    if left_norm == 0 or right_norm == 0:
        return 0.0
    return numerator / (left_norm * right_norm)

