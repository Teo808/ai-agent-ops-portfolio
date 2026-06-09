# Obsidian + Supermemory-Style Memory System Plan

Status: design plan for practical agent memory and personal knowledge workflows.

## Goal

Create a memory system where an AI agent can remember useful context without mixing up sources, projects, or stale information.

## Core Idea

Use Obsidian as a human-readable memory layer and a Supermemory-style recall system as the agent-readable layer.

Obsidian is for browsing, editing, and long-term structure. Supermemory-style recall is for search, project scoping, and fast agent context injection.

## Folder Structure

```text
memory/
  profile/
    stable_facts.md
    preferences.md
  projects/
    hermes-agent/
      setup-notes.md
      issues.md
      lessons.md
    job-search/
      target-roles.md
      application-notes.md
  workflows/
    agent-debugging-checklist.md
    browser-automation-checklist.md
    memory-recall-checklist.md
  archive/
    stale-or-replaced.md
```

## Memory Record Template

```text
Title:

Source:

Project:

Date:

Confidence:

Currentness:

Summary:

Evidence:

When to use:

When not to use:
```

## Recall Rules

- Prefer current project memories over broad personal memories.
- Label whether something is confirmed, inferred, planned, or stale.
- Do not use private facts unless they directly help the task.
- Keep implementation notes separate from preferences.
- Mark old setup instructions as stale after tools or config change.

## Agent Handoff Flow

1. User asks for help with a project.
2. Agent searches project memory first.
3. Agent checks profile/preferences only if relevant.
4. Agent cites which memories shaped the answer.
5. Agent saves a short lesson only after the task is verified.

## Example Use Case

Problem: An AI agent cannot find the right setup note for a broken MCP integration.

Memory workflow:

1. Search `projects/hermes-agent/issues.md`.
2. Check whether the issue is auth, transport, config path, or tool naming.
3. Pull the matching checklist.
4. Run the verification command.
5. Save the final fix as a short lesson with date and source.

## What This Shows

Agent memory is not just storage. It is an operations problem: source quality, scoping, currentness, verification, and handoff all matter.

