from __future__ import annotations

from dataclasses import dataclass

from agents.study_plan_generator import StudyPlan
from iq_layers import WorkContext


@dataclass(frozen=True)
class EngagementPlan:
    reminder_cadence: str
    recommended_slot: str
    message: str


class EngagementAgent:
    def run(self, learner: dict, study_plan: StudyPlan, work_context: WorkContext) -> EngagementPlan:
        if work_context.capacity_level == "constrained":
            cadence = "2 gentle reminders per week"
            tone = "protect focus time and avoid overload"
        elif work_context.capacity_level == "strong":
            cadence = "3 progress reminders per week"
            tone = "encourage steady progress"
        else:
            cadence = "2 to 3 reminders per week"
            tone = "balance progress with workload"

        return EngagementPlan(
            reminder_cadence=cadence,
            recommended_slot=work_context.preferred_slot,
            message=(
                f"Schedule {study_plan.weekly_hours} learning hours in the "
                f"{work_context.preferred_slot.lower()} and {tone}."
            ),
        )

