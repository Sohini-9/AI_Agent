# Reasoning Agents - Enterprise Learning Starter Kit

This is a local, demoable multi-agent project for the **Reasoning Agents** challenge scenario.

The system helps an organisation manage synthetic certification learning programmes using multi-step reasoning across specialised agents.

## What It Demonstrates

- Multi-agent orchestration
- Planner-executor style reasoning
- Grounded retrieval over approved learning content
- Work-context-aware study planning
- Semantic business understanding for roles, certifications, skills, and thresholds
- Assessment and readiness feedback
- Manager-level team insights
- Lightweight evaluation and verifier guardrails

## Important Data Note

All data is synthetic. The project does not use real employee data, real customer data, credentials, or personally identifiable information.

## Agent Architecture

```text
Learner request
-> Learning Path Curator Agent
-> Study Plan Generator Agent
-> Engagement Agent
-> Assessment Agent
-> Verifier Agent
-> Learner report

Manager request
-> Manager Insights Agent
-> Team readiness report
```



## Example Output

The demo produces:

- A learner-level certification plan for `L-1001`
- Grounded citations from synthetic knowledge documents
- Capacity-aware study schedule
- Engagement reminder strategy
- Assessment questions and readiness feedback
- Manager insights for `TEAM-A`

Reports are written to the `reports` folder.



