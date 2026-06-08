from __future__ import annotations

from dataclasses import dataclass

from iq_layers import FabricIQLayer, FoundryIQLayer
from retrieval import RetrievedChunk


@dataclass(frozen=True)
class LearningPath:
    certification_id: str
    certification_name: str
    required_skills: list[str]
    missing_skills: list[str]
    citations: list[RetrievedChunk]


class LearningPathCuratorAgent:
    def __init__(self, foundry_iq: FoundryIQLayer, fabric_iq: FabricIQLayer) -> None:
        self._foundry_iq = foundry_iq
        self._fabric_iq = fabric_iq

    def run(self, learner: dict) -> LearningPath:
        certification = self._fabric_iq.certification_by_id(learner["certification"])
        missing_skills = self._fabric_iq.missing_skills(learner)
        query = f"{learner['role']} {learner['certification']} {' '.join(missing_skills)}"
        citations = self._foundry_iq.retrieve(query, top_k=3)

        return LearningPath(
            certification_id=certification["id"],
            certification_name=certification["name"],
            required_skills=certification["skills"],
            missing_skills=missing_skills,
            citations=citations,
        )

