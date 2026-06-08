from __future__ import annotations

from data_loader import write_report
from orchestrator import CertificationOrchestrator


def main() -> None:
    orchestrator = CertificationOrchestrator()

    learner_report = orchestrator.run_for_learner("L-1001")
    manager_report = orchestrator.run_manager_view("TEAM-A")

    learner_path = write_report("learner_L-1001_report.txt", learner_report)
    manager_path = write_report("manager_TEAM-A_report.txt", manager_report)

    print_title("Reasoning Agents Demo")
    print(learner_report)
    print_title("Manager View")
    print(manager_report)
    print(f"\nReports saved:\n- {learner_path}\n- {manager_path}")


def print_title(title: str) -> None:
    border = "=" * len(title)
    print(f"\n{title}\n{border}")


if __name__ == "__main__":
    main()

