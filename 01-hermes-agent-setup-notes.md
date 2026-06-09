# Hermes / AI Agent Setup Notes

Status: working portfolio note based on hands-on setup, testing, and troubleshooting patterns.

## Goal

Build reliable setup and QA habits for Hermes-style AI agents that run across local machines, messaging surfaces, memory systems, model providers, and external tools.

## Areas I Test

- Provider setup: Nous Portal, OpenRouter, local model endpoints, and OpenAI-compatible APIs.
- Memory behavior: project memory, personal memory, recall quality, source labels, stale memories, and cross-agent handoff.
- MCP/tool integrations: tool discovery, auth, transport errors, server availability, and tool naming clarity.
- Browser automation: page navigation, form filling, screenshots, and failure recovery.
- Messaging surfaces: Telegram/CLI-style usage, continuity across sessions, and readable final responses.
- Workflow persistence: tasks, notes, lessons, retry plans, and status reports.

## Practical Checklist

### Install / Configure

- Confirm the agent starts cleanly.
- Confirm provider credentials are present without exposing secrets.
- Confirm selected model can answer a basic prompt.
- Confirm tool list loads without config errors.
- Confirm memory recall works on a known saved item.

### Break / Debug

- Test missing API key behavior.
- Test unavailable MCP server behavior.
- Test stale memory or wrong project recall.
- Test browser automation on a slow or dynamic page.
- Test repeated task retries and cancellation behavior.

### Document / Improve

- Write the exact failure message.
- Record the command or UI path that reproduced it.
- Record the fix and the verification step.
- Turn repeated fixes into a checklist or skill note.
- Separate confirmed behavior from guesses.

## Example Issue Report Format

```text
Issue:
Memory search returns irrelevant project results.

Environment:
Windows PowerShell, Hermes-style agent, Supermemory-style project memory.

Expected:
Recall should prioritize current project memories when a project scope is selected.

Actual:
Recall includes broad personal history and unrelated project notes.

Reproduction:
1. Search for a project-specific setup error.
2. Include profile summary.
3. Compare project-scoped results against default-scope results.

Fix / Next Step:
Tighten project scoping, add source labels, and rerun the same query.

Verification:
The same query returns current-project setup notes in the top results.
```

## What This Shows

This is the work style I would bring to Hermes Agent deployment: use the system for real tasks, find the sharp edges, explain them clearly, and turn fixes into repeatable operational knowledge.

