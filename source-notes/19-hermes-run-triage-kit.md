# Hermes run triage kit

A small standard-library Python tool for reviewing Hermes Agent runs. It reads a JSONL session export or plain-text log and produces a Markdown operator QA report.

## What it checks

- stale browser references
- tool errors and exceptions
- timeouts
- authentication and permission problems
- rate limits and quotas
- possible secret leakage
- verified success lines
- repeated tool calls that may indicate retry loops

The point is not to judge a run from the final answer alone. A useful report should show what the agent read, which tools appeared, what failed, what was verified, and what the next operator should check.

## Evidence

The source lives at [`demo/hermes_run_triage.py`](../demo/hermes_run_triage.py). It uses only the Python standard library.

I ran four unit tests locally covering JSONL loading, stale browser detection, redaction risk, and report recommendations. The suite passed.

The companion QA note in the local draft package records a real browser workflow where a stale reference was recovered with a fresh snapshot and the sent message was verified in the thread.
