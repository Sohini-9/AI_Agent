from __future__ import annotations

from dataclasses import dataclass

from iq_layers import FabricIQLayer, WorkIQLayer


@dataclass(frozen=True)
class ManagerInsights:
    team: str
    ready_count: int
    at_risk_count: int
    insights: list[str]


class ManagerInsightsAgent:
    def __init__(self, fabric_iq: FabricIQLayer, work_iq: WorkIQLayer) -> None:
        self._fabric_iq = fabric_iq
        self._work_iq = work_iq

    def run(self, learners: list[dict], team: str) -> ManagerInsights:
        team_learners = [learner for learner in learners if learner["team"] == team]
        ready_count = 0
        insights: list[str] = []

        for learner in team_learners:
            gap = self._fabric_iq.readiness_gap(learner)
            context = self._work_iq.context_for(learner["employee_id"])
            if gap == 0:
                ready_count += 1
            if gap > 0 or context.capacity_level == "constrained":
                insights.append(
                    f"{learner['learner_id']} has readiness gap {gap} and {context.capacity_level} work capacity."
                )

        return ManagerInsights(
            team=team,
            ready_count=ready_count,
            at_risk_count=len(team_learners) - ready_count,
            insights=insights or ["Team is broadly on track for certification readiness."],
        )

