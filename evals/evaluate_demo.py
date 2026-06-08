from __future__ import annotations

import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_DIR / "src"
sys.path.insert(0, str(SRC_DIR))

from orchestrator import CertificationOrchestrator  # noqa: E402


def main() -> None:
    orchestrator = CertificationOrchestrator()
    report = orchestrator.run_for_learner("L-1001")

    checks = {
        "mentions synthetic data": "Synthetic Data" in report,
        "includes citations": "source=" in report,
        "shows all core agents": all(
            label in report
            for label in [
                "Learning Path Curator",
                "Study Plan Generator",
                "Engagement Agent",
                "Assessment Agent",
            ]
        ),
        "has final reasoning outcome": "Reasoning Outcome" in report,
    }

    print("Evaluation Results")
    print("==================")
    for name, passed in checks.items():
        print(f"{name}: {'PASS' if passed else 'FAIL'}")

    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()

