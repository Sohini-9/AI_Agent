from __future__ import annotations

from agents.assessment_agent import AssessmentAgent
from agents.engagement_agent import EngagementAgent
from agents.learning_path_curator import LearningPathCuratorAgent
from agents.manager_insights_agent import ManagerInsightsAgent
from agents.study_plan_generator import StudyPlanGeneratorAgent
from agents.verifier_agent import VerifierAgent
from data_loader import load_json, load_text
from iq_layers import FabricIQLayer, FoundryIQLayer, WorkIQLayer
from retrieval import KeywordVectorIndex, chunk_markdown


class CertificationOrchestrator:
    def __init__(self) -> None:
        semantic_model = load_json("semantic_model.json")
        work_signals = load_json("work_signals.json")
        knowledge_text = load_text("knowledge_docs.md")
        chunks = chunk_markdown(knowledge_text, source="knowledge_docs.md")

        self.learners = load_json("learners.json")
        self.foundry_iq = FoundryIQLayer(KeywordVectorIndex(chunks))
        self.fabric_iq = FabricIQLayer(semantic_model)
        self.work_iq = WorkIQLayer(work_signals)

        self.curator = LearningPathCuratorAgent(self.foundry_iq, self.fabric_iq)
        self.planner = StudyPlanGeneratorAgent(self.fabric_iq)
        self.engagement = EngagementAgent()
        self.assessment = AssessmentAgent(self.foundry_iq, self.fabric_iq)
        self.manager = ManagerInsightsAgent(self.fabric_iq, self.work_iq)
        self.verifier = VerifierAgent()

    def run_for_learner(self, learner_id: str) -> str:
        learner = self._find_learner(learner_id)
        work_context = self.work_iq.context_for(learner["employee_id"])
        learning_path = self.curator.run(learner)
        study_plan = self.planner.run(learner, learning_path, work_context)
        engagement_plan = self.engagement.run(learner, study_plan, work_context)
        assessment = self.assessment.run(learner)

        report = self._format_learner_report(
            learner,
            work_context,
            learning_path,
            study_plan,
            engagement_plan,
            assessment,
        )
        warnings = self.verifier.run(report)

        if warnings:
            report += "\n\nVerifier Warnings:\n" + "\n".join(f"- {warning}" for warning in warnings)
        return report

    def run_manager_view(self, team: str) -> str:
        insights = self.manager.run(self.learners, team)
        lines = [
            "Manager Insights Report (Synthetic Data)",
            f"Team: {insights.team}",
            f"Ready learners: {insights.ready_count}",
            f"At-risk learners: {insights.at_risk_count}",
            "Insights:",
            *[f"- {item}" for item in insights.insights],
        ]
        return "\n".join(lines)

    def _find_learner(self, learner_id: str) -> dict:
        for learner in self.learners:
            if learner["learner_id"] == learner_id:
                return learner
        raise ValueError(f"Unknown learner: {learner_id}")

    def _format_learner_report(
        self,
        learner: dict,
        work_context,
        learning_path,
        study_plan,
        engagement_plan,
        assessment,
    ) -> str:
        citation_lines = [
            f"- {item.text} (source={item.source}, score={item.score})"
            for item in learning_path.citations
        ]

        return "\n".join(
            [
                "Reasoning Agents Learner Report (Synthetic Data)",
                f"Learner: {learner['learner_id']}",
                f"Role: {learner['role']}",
                f"Certification: {learning_path.certification_id} - {learning_path.certification_name}",
                "",
                "Agent 1 - Learning Path Curator:",
                f"Required skills: {', '.join(learning_path.required_skills)}",
                f"Missing skills: {', '.join(learning_path.missing_skills) or 'None'}",
                "Citations:",
                *citation_lines,
                "",
                "Agent 2 - Study Plan Generator:",
                f"Weekly hours: {study_plan.weekly_hours}",
                f"Duration: {study_plan.duration_weeks} week(s)",
                f"Rationale: {study_plan.rationale}",
                *[f"- {milestone}" for milestone in study_plan.milestones],
                "",
                "Agent 3 - Engagement Agent:",
                f"Reminder cadence: {engagement_plan.reminder_cadence}",
                f"Recommended slot: {engagement_plan.recommended_slot}",
                f"Message: {engagement_plan.message}",
                "",
                "Agent 4 - Assessment Agent:",
                f"Readiness score: {assessment.readiness_score}",
                f"Passed readiness check: {assessment.passed}",
                "Grounded practice questions:",
                *[f"- {question}" for question in assessment.questions],
                "Feedback:",
                *[f"- {item}" for item in assessment.feedback],
                "",
                "Reasoning Outcome:",
                "Recommend exam scheduling." if assessment.passed else "Loop back into preparation workflow.",
            ]
        )

