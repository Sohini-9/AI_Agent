from __future__ import annotations

from dataclasses import dataclass

from iq_layers import FabricIQLayer, FoundryIQLayer


@dataclass(frozen=True)
class AssessmentResult:
    readiness_score: int
    passed: bool
    questions: list[str]
    feedback: list[str]


class AssessmentAgent:
    def __init__(self, foundry_iq: FoundryIQLayer, fabric_iq: FabricIQLayer) -> None:
        self._foundry_iq = foundry_iq
        self._fabric_iq = fabric_iq

    def run(self, learner: dict) -> AssessmentResult:
        certification = self._fabric_iq.certification_by_id(learner["certification"])
        missing_skills = self._fabric_iq.missing_skills(learner)
        readiness_gap = self._fabric_iq.readiness_gap(learner)
        citations = self._foundry_iq.retrieve(f"{learner['certification']} assessment readiness", top_k=2)

        readiness_score = learner["practice_score_avg"] - (5 if missing_skills else 0)
        passed = readiness_score >= certification["pass_threshold"]

        questions = [
            f"Explain one production use case for {skill} in {certification['id']}."
            for skill in (missing_skills or certification["skills"][:2])
        ]
        feedback = [
            f"Practice score gap to threshold: {readiness_gap} points.",
            f"Grounding sources used: {', '.join(item.source for item in citations) or 'none'}."
        ]

        if missing_skills:
            feedback.append(f"Focus next on: {', '.join(missing_skills)}.")
        else:
            feedback.append("Core skills are complete; proceed to final practice assessment.")

        return AssessmentResult(
            readiness_score=readiness_score,
            passed=passed,
            questions=questions,
            feedback=feedback,
        )

