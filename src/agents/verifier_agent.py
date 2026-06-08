from __future__ import annotations


class VerifierAgent:
    """Lightweight guardrail that checks reports for grounding and safe synthetic-data framing."""

    def run(self, report: str) -> list[str]:
        warnings: list[str] = []

        if "Synthetic" not in report and "synthetic" not in report:
            warnings.append("Report should state that the data is synthetic.")
        if "citations" not in report.lower() and "source" not in report.lower():
            warnings.append("Report should include grounding sources or citations.")
        if "password" in report.lower() or "secret" in report.lower():
            warnings.append("Report may contain sensitive secret-like content.")

        return warnings

