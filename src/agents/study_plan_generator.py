from __future__ import annotations

from dataclasses import dataclass

from agents.learning_path_curator import LearningPath
from iq_layers import FabricIQLayer, WorkContext


@dataclass(frozen=True)
class StudyPlan:
    weekly_hours: int
    duration_weeks: int
    milestones: list[str]
    rationale: str


class StudyPlanGeneratorAgent:
    def __init__(self, fabric_iq: FabricIQLayer) -> None:
        self._fabric_iq = fabric_iq

    def run(self, learner: dict, learning_path: LearningPath, work_context: WorkContext) -> StudyPlan:
        certification = self._fabric_iq.certification_by_id(learning_path.certification_id)
        remaining_hours = max(4, certification["recommended_hours"] - learner["hours_studied"])

        if work_context.capacity_level == "constrained":
            weekly_hours = 4
        elif work_context.capacity_level == "strong":
            weekly_hours = 8
        else:
            weekly_hours = 6

        duration_weeks = max(1, (remaining_hours + weekly_hours - 1) // weekly_hours)
        milestones = [
            f"Week {index + 1}: study {skill} and complete one practice checkpoint"
            for index, skill in enumerate(learning_path.missing_skills or learning_path.required_skills[:2])
        ]
        milestones.append("Final week: complete readiness assessment and review weak areas")

        return StudyPlan(
            weekly_hours=weekly_hours,
            duration_weeks=duration_weeks,
            milestones=milestones,
            rationale=(
                f"Plan uses {work_context.capacity_level} capacity, "
                f"{work_context.focus_hours} focus hours/week, and {remaining_hours} remaining study hours."
            ),
        )

