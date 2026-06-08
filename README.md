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

## Microsoft IQ Mapping

This local implementation mirrors the challenge IQ layers:

- **Foundry IQ concept:** `FoundryIQLayer` retrieves grounded learning content from synthetic documents.
- **Fabric IQ concept:** `FabricIQLayer` models semantic relationships between roles, certifications, skills, recommended hours, and readiness thresholds.
- **Work IQ concept:** `WorkIQLayer` uses synthetic meeting load, focus hours, and preferred learning slots to adapt schedules and reminders.

## Project Structure

```text
reasoning_agents_learning
├── data
│   ├── knowledge_docs.md
│   ├── learners.json
│   ├── semantic_model.json
│   └── work_signals.json
├── evals
│   └── evaluate_demo.py
├── reports
├── src
│   ├── agents
│   │   ├── assessment_agent.py
│   │   ├── engagement_agent.py
│   │   ├── learning_path_curator.py
│   │   ├── manager_insights_agent.py
│   │   ├── study_plan_generator.py
│   │   └── verifier_agent.py
│   ├── data_loader.py
│   ├── iq_layers.py
│   ├── main.py
│   ├── orchestrator.py
│   └── retrieval.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Run The Demo

From this folder:

```bash
python src/main.py
```

Run the evaluation checks:

```bash
python evals/evaluate_demo.py
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

## How To Explain This In An Interview

I built a multi-agent enterprise learning system for certification readiness. A curator agent retrieves grounded learning content, a planning agent converts role and certification requirements into a study plan, an engagement agent adapts reminders using synthetic work-context signals, and an assessment agent evaluates readiness using semantic certification thresholds. A manager insights agent aggregates team-level risk and readiness. The solution uses synthetic data only and includes a verifier and evaluation script to demonstrate responsible, production-minded agent design.

## Cloud Extension Path

For a Microsoft Foundry version:

- Replace `KeywordVectorIndex` with Foundry IQ-backed retrieval.
- Replace local orchestration with Microsoft Agent Framework or Foundry Agent Service.
- Use managed identity and environment variables instead of secrets in code.
- Add telemetry, traces, and formal evaluation datasets.
- Containerise the app for hosted agent deployment.

