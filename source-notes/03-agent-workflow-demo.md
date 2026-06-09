# Small Agent Workflow Demo

Status: runnable local demo using Python standard library only.

## Goal

Show a simple AI agent operations workflow:

1. Accept a deployment/support scenario.
2. Classify the likely issue.
3. Choose practical checks.
4. Produce a support-ready report.

This is not an LLM model demo. It is a workflow design demo for agent deployment and support operations.

## Recruiter / Hiring Manager Summary

The demo shows how I approach messy agent issues: classify the failure layer, choose small checks, and produce a report another operator or engineer can act on. It is deliberately small so the logic is easy to review.

## Run

From this folder:

```powershell
python .\demo\agent_workflow_demo.py
```

## What It Demonstrates

- Clear issue intake.
- Routing an agent problem into likely categories.
- Producing verification steps.
- Writing an operator-friendly report.
- Separating confirmed checks from recommended next steps.

## Categories Covered

| Category | Example symptoms |
| --- | --- |
| `memory_scope` | Wrong project recall, stale context, broad personal history |
| `tool_config` | Missing MCP tool, auth mismatch, transport/config errors |
| `browser_workflow` | Page state, login, selector, CAPTCHA, or form issues |
| `provider_routing` | Wrong model, endpoint, fallback, or OpenAI-compatible provider issue |

## Example Output

```text
Scenario: Hermes Agent cannot recall project-specific setup notes after a tool config change.
Likely category: memory_scope
Priority: high

Recommended checks:
- Confirm the active project/container scope.
- Run the same recall query with and without profile context.
- Check whether stale global memories are outranking project memories.
- Verify the final answer cites the project-specific source.

Operator report:
The issue appears related to memory scoping rather than model quality...
```

## Why This Matters

Forward deployed agent work often means turning ambiguous user reports into concrete debugging paths. The value is not only writing code; it is making the system easier to operate, support, and improve.

## Hiring Signal

This is the operational muscle I would bring to Hermes Agent: do not guess, do not hand-wave, and do not hide uncertainty. Route the issue, run the smallest useful check, and write the result so the next person can move faster.
