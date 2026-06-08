from __future__ import annotations

from dataclasses import dataclass

from retrieval import KeywordVectorIndex, RetrievedChunk


@dataclass(frozen=True)
class WorkContext:
    meeting_hours: int
    focus_hours: int
    preferred_slot: str
    capacity_level: str


class FoundryIQLayer:
    """Grounding layer for approved synthetic learning content."""

    def __init__(self, index: KeywordVectorIndex) -> None:
        self._index = index

    def retrieve(self, query: str, top_k: int = 4) -> list[RetrievedChunk]:
        return self._index.search(query, top_k=top_k)


class FabricIQLayer:
    """Semantic business layer for roles, certifications, skills, and thresholds."""

    def __init__(self, semantic_model: dict) -> None:
        self._semantic_model = semantic_model

    def certification_for_role(self, role: str) -> dict:
        certification_id = self._semantic_model["role_certification_map"][role]
        return self.certification_by_id(certification_id)

    def certification_by_id(self, certification_id: str) -> dict:
        for certification in self._semantic_model["certifications"]:
            if certification["id"] == certification_id:
                return certification
        raise ValueError(f"Unknown certification: {certification_id}")

    def missing_skills(self, learner: dict) -> list[str]:
        certification = self.certification_by_id(learner["certification"])
        completed = set(learner["completed_modules"])
        return [skill for skill in certification["skills"] if skill not in completed]

    def readiness_gap(self, learner: dict) -> int:
        certification = self.certification_by_id(learner["certification"])
        return max(0, certification["pass_threshold"] - learner["practice_score_avg"])


class WorkIQLayer:
    """Work-context layer for capacity-aware planning and engagement."""

    def __init__(self, work_signals: list[dict]) -> None:
        self._signals = {item["employee_id"]: item for item in work_signals}

    def context_for(self, employee_id: str) -> WorkContext:
        signal = self._signals[employee_id]
        meeting_hours = signal["meeting_hours_per_week"]
        focus_hours = signal["focus_hours_per_week"]

        if meeting_hours > 20 or focus_hours < 12:
            capacity_level = "constrained"
        elif focus_hours >= 16:
            capacity_level = "strong"
        else:
            capacity_level = "moderate"

        return WorkContext(
            meeting_hours=meeting_hours,
            focus_hours=focus_hours,
            preferred_slot=signal["preferred_learning_slot"],
            capacity_level=capacity_level,
        )

