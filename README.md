# AI Agent Operations Portfolio - Matteo Stincone

Portfolio for Forward Deployed Engineer / AI Agent Operations roles. Focused on the practical deployment layer: setup, tools, memory, browser workflows, provider routing, debugging, and documentation.

**Live site:** https://teo808.github.io/ai-agent-ops-portfolio/

---

## What this is

Applying to Nous Research for the Forward Deployed Engineer role. Hermes Agent specifically is the reason. This portfolio is built around that work: deploying agents, testing real workflows, finding what breaks, and writing the fix clearly enough for the next person to follow.

Not the ML research angle. The angle is that these systems get used in real environments, and that layer gets messy fast. Setup is fragile, docs leave things out, and the first few failures do not always turn into a clear path for the next person. That is what this portfolio addresses.

## Role Alignment

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

## Run The Demo

```
python demo/agent_workflow_demo.py
python demo/browser_preflight_report.py --all
python demo/action_receipt_report.py --all
```

No dependencies. Standard library only.

## Fast Review Path

Five minutes:

1. [Candidate Profile](https://teo808.github.io/ai-agent-ops-portfolio/candidate-profile.html) - positioning and what I can point to
2. [Setup Notes](https://teo808.github.io/ai-agent-ops-portfolio/setup-notes.html) - how I think about Hermes Agent deployment testing
3. [Browser automation preflight](https://teo808.github.io/ai-agent-ops-portfolio/browser-automation-preflight.html) - how I check account safety before real browser actions
4. [Support handoff signal log](https://teo808.github.io/ai-agent-ops-portfolio/support-handoff-signal.html) - what recent workflow QA engagement keeps pointing back to
5. [Social signal triage loop](https://teo808.github.io/ai-agent-ops-portfolio/social-signal-triage.html) - how I decide whether to reply, wait, or turn a signal into proof
6. [Verified no-action rule](https://teo808.github.io/ai-agent-ops-portfolio/verified-no-action.html) - how I avoid claiming sends, posts, or applications when proof is missing
7. [Relationship outreach cooldown rule](https://teo808.github.io/ai-agent-ops-portfolio/outreach-cooldown-rule.html) - how I avoid repeat-contacting the same person or company when waiting is the better move
8. [Browser preflight decision demo](https://teo808.github.io/ai-agent-ops-portfolio/preflight-decision-demo.html) - a small executable send or stop check
9. [Action receipt report demo](https://teo808.github.io/ai-agent-ops-portfolio/action-receipt-report.html) - how I prove what actually happened after a risky workflow action
10. Run the demo scripts

---

Matteo Stincone - teo8js@gmail.com
