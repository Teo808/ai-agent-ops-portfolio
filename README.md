# AI agent operations portfolio | Matteo Stincone

Portfolio for AI support, workflow operations, technical support, implementation support, and Forward Deployed Engineer roles. The work focuses on the practical layer around AI systems: setup, tools, memory, browser workflows, provider behavior, debugging, and documentation.

**Live site:** https://teo808.github.io/ai-agent-ops-portfolio/

---

## What this is

This portfolio shows how I test AI workflows in real environments, find the layer that failed, and write the next safe step clearly enough for another person to follow.

I am not presenting myself as an ML researcher. My lane is the practical work around AI products: setup, tool and provider troubleshooting, workflow QA, browser automation, support handoffs, and documentation that holds up after the demo ends.

## Role alignment

| What the role needs | What I can show |
| --- | --- |
| Deploy and adapt Hermes Agent Enterprise | Hermes-style setup notes and operational testing checklist |
| Integrate APIs, tools, and internal systems | MCP/tool integration and provider-routing test coverage |
| Debug production issues across layers | Workflow demo that separates memory, tools, browser, provider, and config failures |
| Document deployment issues and fixes | Setup guides, issue reports, and debugging notes others can follow |
| Improve reliability from the field | Repeatable verification steps, failure-report templates, and product feedback |

## Portfolio Pieces

### 1. Hermes / AI Agent Setup Notes

[View on the live site](https://teo808.github.io/ai-agent-ops-portfolio/setup-notes.html)

How to test agent setup: provider config, MCP/tool integrations, memory behavior, browser automation, and failure reporting. The goal is a checklist someone else can run, not just notes that only make sense to the person who wrote them.

### 2. Memory System Plan

[View on the live site](https://teo808.github.io/ai-agent-ops-portfolio/memory-system.html)

A design for project-scoped, source-labeled agent memory. Covers how to prevent stale global context from overriding current project facts, and how to keep memory auditable.

### 3. Agent Workflow Demo

[View on the live site](https://teo808.github.io/ai-agent-ops-portfolio/workflow-demo.html) - [Python script](./demo/agent_workflow_demo.py)

A pure standard-library Python demo that takes an ambiguous agent failure, classifies the likely layer (memory, tools, browser, provider), and produces a structured operator report.

### 4. Agent recovery packet

[View on the live site](https://teo808.github.io/ai-agent-ops-portfolio/agent-recovery-packet.html) - [Markdown source](./source-notes/04-agent-recovery-packet.md)

A short checklist for what an agent should leave behind when it cannot finish a workflow: what it tried, what changed, what is still open, what blocked it, what the user should do next, and what the next run should check first.

### 5. Browser automation preflight

[View on the live site](https://teo808.github.io/ai-agent-ops-portfolio/browser-automation-preflight.html) - [Markdown source](./source-notes/05-browser-automation-preflight.md)

A practical checklist for browser automation before an agent acts inside signed in accounts or real workflows. It covers context proof, account proof, action boundaries, blockers, verification, and handoffs.

### 6. Support handoff signal log

[View on the live site](https://teo808.github.io/ai-agent-ops-portfolio/support-handoff-signal.html) - [Markdown source](./source-notes/06-support-handoff-signal.md)

A short public note on what useful AI workflow QA comments keep pointing back to: state, blockers, and clean handoffs.

### 7. Social signal triage loop

[View on the live site](https://teo808.github.io/ai-agent-ops-portfolio/social-signal-triage.html) - [Markdown source](./source-notes/07-social-signal-triage.md)

A practical loop for turning comments, replies, profile views, and recruiter signals into cleaner proof or a better next step.

### 8. Verified no-action rule

[View on the live site](https://teo808.github.io/ai-agent-ops-portfolio/verified-no-action.html) - [Markdown source](./source-notes/08-verified-no-action.md)

A short rule for stopping before a real click when the browser, account, boundary, or result cannot be verified.

### 9. Relationship outreach cooldown rule

[View on the live site](https://teo808.github.io/ai-agent-ops-portfolio/outreach-cooldown-rule.html) - [Markdown source](./source-notes/09-outreach-cooldown-rule.md)

A short rule for checking outreach history before sending another recruiter, company, or social message.

### 10. Browser preflight decision demo

[View on the live site](https://teo808.github.io/ai-agent-ops-portfolio/preflight-decision-demo.html) - [Python script](./demo/browser_preflight_report.py) - [Markdown source](./source-notes/10-browser-preflight-decision-demo.md)

A small Python demo for deciding whether browser automation should send, submit, publish, or stop based on context proof, account proof, action boundary, blocker state, and result proof.

### 11. Action receipt report demo

[View on the live site](https://teo808.github.io/ai-agent-ops-portfolio/action-receipt-report.html) - [Python script](./demo/action_receipt_report.py) - [Markdown source](./source-notes/11-action-receipt-report.md)

A small Python demo for building a verification receipt after a workflow sends, submits, publishes, connects, or messages from a real account.

### 12. Browser attach health check demo

[View on the live site](https://teo808.github.io/ai-agent-ops-portfolio/browser-attach-health-check.html) - [Python script](./demo/browser_attach_health_check.py) - [Markdown source](./source-notes/12-browser-attach-health-check.md)

A small Python demo for deciding whether real-account browser automation can continue, open the target page, or stop before any risky action.

### 13. Application run gate demo

[View on the live site](https://teo808.github.io/ai-agent-ops-portfolio/application-run-gate.html) - [Python script](./demo/application_run_gate.py) - [Markdown source](./source-notes/13-application-run-gate.md)

A small Python demo for deciding whether a job lead should be applied to, staged, saved, or rejected before a workflow touches a real account.

### 14. Session tool health demo

[View on the live site](https://teo808.github.io/ai-agent-ops-portfolio/session-tool-health.html) - [Python script](./demo/session_tool_health.py) - [Markdown source](./source-notes/14-session-tool-health.md)

A small Python demo for separating installed tool health from active session proof before a workflow touches a real account.

### 15. Real-account automation incident runbook

[View on the live site](https://teo808.github.io/ai-agent-ops-portfolio/real-account-automation-incident-runbook.html) - [Python script](./demo/real_account_incident_runbook.py) - [Markdown source](./source-notes/15-real-account-automation-incident-runbook.md)

A short runbook for handling browser or automation failures before a workflow touches a real account.

### 16. Source and status handoff checklist

[View on the live site](https://teo808.github.io/ai-agent-ops-portfolio/source-status-handoff-checklist.html) - [Python script](./demo/source_status_handoff_checklist.py) - [Markdown source](./source-notes/16-source-status-handoff-checklist.md)

A short checklist for making AI support handoffs prove source, status, permission state, last action, open work, and next owner.

### 17. Cross-agent handoff checklist

[View on the live site](https://teo808.github.io/ai-agent-ops-portfolio/cross-agent-handoff-checklist.html) - [Python script](./demo/cross_agent_handoff_checklist.py) - [Markdown source](./source-notes/17-cross-agent-handoff-checklist.md)

A practical checklist for passing a support or workflow case from one agent to another without making the customer repeat the story. It checks the current goal, state, actions already taken, open risk, next owner, and the first safe resume check.

### 18. Workflow reliability case study

[View on the live site](https://teo808.github.io/ai-agent-ops-portfolio/workflow-reliability-case-study.html)

A featured case study showing how I diagnosed a locked real-account browser workflow, protected the user's normal session, removed only stale scheduled owners, and verified recovery with an operator receipt.

### 19. AI workflow QA test matrix

[View on the live site](https://teo808.github.io/ai-agent-ops-portfolio/ai-workflow-qa-test-matrix.html) - [Python script](./demo/ai_workflow_qa_test_matrix.py) - [Markdown source](./source-notes/18-ai-workflow-qa-test-matrix.md)

A small test matrix for source freshness, permission boundaries, missing fields, interrupted sessions, and human approval. It focuses on the evidence and recovery path around an AI support workflow, not only the final answer.

### 20. Hermes run triage kit

[View on the live site](https://teo808.github.io/ai-agent-ops-portfolio/hermes-run-triage-kit.html) - [Python script](./demo/hermes_run_triage.py) - [Project notes](./source-notes/19-hermes-run-triage-kit.md)

A small standard-library Python tool that turns a Hermes session export or plain-text log into a Markdown operator QA report. It checks stale browser refs, tool errors, timeouts, permission issues, rate limits, possible secret leakage, retry loops, and verified success lines.

## Run The Demo

```
python demo/agent_workflow_demo.py
python demo/browser_preflight_report.py --all
python demo/action_receipt_report.py --all
python demo/browser_attach_health_check.py --all
python demo/application_run_gate.py --all
python demo/session_tool_health.py --all
python demo/real_account_incident_runbook.py --all
python demo/source_status_handoff_checklist.py --all
python demo/cross_agent_handoff_checklist.py --all
python demo/ai_workflow_qa_test_matrix.py --all
python demo/hermes_run_triage.py examples/hermes_sample_session.jsonl --title "Hermes Run" --out report.md
```

No dependencies. Standard library only.

## Fast Review Path

Five minutes:

1. [Candidate Profile](https://teo808.github.io/ai-agent-ops-portfolio/candidate-profile.html) - positioning and what I can point to
2. [Workflow reliability case study](https://teo808.github.io/ai-agent-ops-portfolio/workflow-reliability-case-study.html) - a real diagnosis, scoped repair, and verification receipt
3. [Setup Notes](https://teo808.github.io/ai-agent-ops-portfolio/setup-notes.html) - how I think about Hermes Agent deployment testing
4. [Browser automation preflight](https://teo808.github.io/ai-agent-ops-portfolio/browser-automation-preflight.html) - how I check account safety before real browser actions
5. [Action receipt report demo](https://teo808.github.io/ai-agent-ops-portfolio/action-receipt-report.html) - how I prove what actually happened after a risky workflow action
6. [Cross-agent handoff checklist](https://teo808.github.io/ai-agent-ops-portfolio/cross-agent-handoff-checklist.html) - how I pass a live support or workflow case between agents without losing state
7. [Hermes run triage kit](https://teo808.github.io/ai-agent-ops-portfolio/hermes-run-triage-kit.html) - how I turn a messy session log into a focused operator QA report
8. Run the demo scripts

---

Matteo Stincone - teo8js@gmail.com
