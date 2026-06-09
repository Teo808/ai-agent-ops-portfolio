#!/usr/bin/env python3
"""
Agent failure triage -- classify a deployment/support scenario and produce an operator report.

Usage:
    python demo/agent_workflow_demo.py              # default scenario
    python demo/agent_workflow_demo.py --all        # all four example scenarios
    python demo/agent_workflow_demo.py --scenario 3 # specific scenario by number
    python demo/agent_workflow_demo.py --verbose    # include category scores
"""

import argparse
from dataclasses import dataclass, field


@dataclass
class Scenario:
    title: str
    symptoms: list
    environment: list
    tags: list = field(default_factory=list)


SCENARIOS = [
    Scenario(
        title="Hermes Agent returns stale context after an MCP config change",
        symptoms=[
            "Recall pulls broad personal history instead of the active project.",
            "Agent answers a setup question with a fix from a different project.",
            "Behavior changed right after a recent MCP/provider reconfiguration.",
        ],
        environment=[
            "Windows PowerShell",
            "Hermes Agent",
            "Supermemory-style project memory",
            "MCP tools configured",
        ],
        tags=["memory", "recall", "project", "mcp"],
    ),
    Scenario(
        title="Browser automation fails silently on the second page load",
        symptoms=[
            "First navigation succeeds but the second page returns empty content.",
            "No error is thrown -- the agent continues with blank context.",
            "Only reproducible when the session has been running more than 10 minutes.",
        ],
        environment=[
            "Hermes Agent with computer-use",
            "Chrome browser",
            "Session timeout not configured",
        ],
        tags=["browser", "page", "session", "selector"],
    ),
    Scenario(
        title="MCP tool passes the health check but fails on real calls",
        symptoms=[
            "Tool appears in the tool list and reports as connected.",
            "Actual calls return permission errors.",
            "A second credential set was added recently.",
        ],
        environment=[
            "Hermes Agent",
            "MCP server v0.4",
            "Two credential sets configured",
        ],
        tags=["tool", "auth", "mcp", "config"],
    ),
    Scenario(
        title="Provider silently switches models mid-conversation",
        symptoms=[
            "Responses become shorter and noticeably less capable after the first few turns.",
            "No error message -- the session looks normal.",
            "Token usage drops sharply at the point behavior changes.",
        ],
        environment=[
            "OpenRouter",
            "Hermes-3 as primary model",
            "Fallback configured for rate limits",
        ],
        tags=["provider", "model", "openrouter", "fallback"],
    ),
]

CHECKS = {
    "memory_scope": [
        "Confirm the active project scope -- check which container the agent is reading from.",
        "Run the same recall query with and without profile context loaded.",
        "Check whether stale global memories are outranking project-scoped ones.",
        "Verify the response cites a project-specific source, not personal history.",
        "Test whether the behavior is consistent or depends on how the query is phrased.",
    ],
    "tool_config": [
        "List available tools and confirm the expected tool name is present.",
        "Check auth state -- confirm presence without printing secrets.",
        "Verify config path, transport type, and server version.",
        "Run the smallest possible tool call and capture the exact error.",
        "Test with a fresh session to rule out session-state corruption.",
    ],
    "browser_workflow": [
        "Confirm the target page loads correctly in a normal browser.",
        "Capture a screenshot or accessibility tree at the failure point.",
        "Check for login walls, CAPTCHAs, dynamic selectors, or blocked popups.",
        "Add explicit waits between navigation steps and retest.",
        "Check whether the failure is session-age dependent.",
    ],
    "provider_routing": [
        "Confirm the selected model and provider are available right now.",
        "Run a minimal one-turn prompt directly against the provider.",
        "Check base URL and model name formatting for the OpenAI-compatible endpoint.",
        "Look for rate-limit headers or fallback triggers in the response metadata.",
        "Compare behavior against a known working provider.",
    ],
}

# Weighted keyword matching per category.
# Higher weight = stronger signal that a scenario belongs to this category.
WEIGHTS = {
    "memory_scope":    {"memory": 3, "recall": 3, "project": 2, "stale": 2, "context": 1, "history": 1},
    "tool_config":     {"tool": 3, "mcp": 3, "auth": 2, "transport": 2, "config": 2, "permission": 2},
    "browser_workflow":{"browser": 3, "page": 2, "selector": 2, "captcha": 2, "session": 1, "form": 1},
    "provider_routing":{"provider": 3, "model": 2, "openrouter": 3, "fallback": 2, "endpoint": 2, "rate": 2},
}


def score_categories(scenario):
    text = " ".join(
        [scenario.title] + scenario.symptoms + scenario.environment + scenario.tags
    ).lower()
    return {
        cat: sum(weight for term, weight in terms.items() if term in text)
        for cat, terms in WEIGHTS.items()
    }


def classify(scenario):
    scores = score_categories(scenario)
    primary = max(scores, key=lambda c: scores[c])
    return primary, scores


def build_report(scenario, verbose=False):
    category, scores = classify(scenario)
    checks = CHECKS[category]

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top, second = sorted_scores[0], sorted_scores[1]
    ambiguous = top[1] > 0 and (top[1] - second[1]) <= 2
    priority = "high" if category in {"memory_scope", "tool_config"} and not ambiguous else "medium"

    lines = [
        "Scenario:  " + scenario.title,
        "Category:  " + category,
        "Priority:  " + priority,
    ]

    if ambiguous and second[1] > 0:
        lines.append(
            "Note:      also consistent with " + second[0] + " -- check both if primary checks don't resolve it."
        )

    if verbose:
        lines.append("Scores:    " + str(dict(sorted_scores)))

    lines += [
        "",
        "Symptoms:",
    ]
    for s in scenario.symptoms:
        lines.append("  " + s)

    lines += ["", "Environment:"]
    for e in scenario.environment:
        lines.append("  " + e)

    lines += ["", "Checks:"]
    for i, c in enumerate(checks):
        lines.append("  " + str(i + 1) + ". " + c)

    lines += [
        "",
        "Operator note:",
        "  Reproduce the symptom first. Then run the smallest check that isolates",
        "  which layer is responsible. Write down what you tried and what it returned",
        "  so the next person doesn't have to start from scratch.",
    ]

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Agent failure triage -- classify a scenario and produce a structured operator report.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="  " + str(len(SCENARIOS)) + " scenarios available: memory scope, browser workflow, tool config, provider routing.",
    )
    parser.add_argument("--all", action="store_true", help="Run all example scenarios.")
    parser.add_argument(
        "--scenario",
        type=int,
        choices=range(1, len(SCENARIOS) + 1),
        metavar="N (1-" + str(len(SCENARIOS)) + ")",
        help="Run a specific example scenario.",
    )
    parser.add_argument("--verbose", action="store_true", help="Show category scores.")
    args = parser.parse_args()

    divider = "-" * 64

    if args.all:
        for i, scenario in enumerate(SCENARIOS, 1):
            print("\n" + divider)
            print("Scenario " + str(i) + " of " + str(len(SCENARIOS)))
            print(divider)
            print(build_report(scenario, verbose=args.verbose))
        print()
    elif args.scenario:
        print(build_report(SCENARIOS[args.scenario - 1], verbose=args.verbose))
    else:
        print(build_report(SCENARIOS[0], verbose=args.verbose))
        print("\nRun with --all to see all " + str(len(SCENARIOS)) + " scenarios, or --help for options.")


if __name__ == "__main__":
    main()
