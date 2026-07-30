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

## Run The Demo

```
python demo/agent_workflow_demo.py
```

No dependencies. Standard library only.

## Fast Review Path

Five minutes:

1. [Candidate Profile](https://teo808.github.io/ai-agent-ops-portfolio/candidate-profile.html) - positioning and what I can point to
2. [Setup Notes](https://teo808.github.io/ai-agent-ops-portfolio/setup-notes.html) - how I think about Hermes Agent deployment testing
3. [Browser automation preflight](https://teo808.github.io/ai-agent-ops-portfolio/browser-automation-preflight.html) - how I check account safety before real browser actions
4. Run the demo script

---

Matteo Stincone - teo8js@gmail.com
