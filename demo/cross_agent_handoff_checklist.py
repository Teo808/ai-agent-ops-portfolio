#!/usr/bin/env python
"""Cross-agent handoff checklist demo.

Check whether a support or workflow handoff contains enough current state for
the next agent to continue without making the user repeat the whole story.

Usage:
    python demo/cross_agent_handoff_checklist.py
    python demo/cross_agent_handoff_checklist.py --all
    python demo/cross_agent_handoff_checklist.py --json
"""

import argparse
import json
from dataclasses import asdict, dataclass


@dataclass
class HandoffCase:
    name: str
    current_goal: str
    state: str
    actions_taken: str
    open_risk: str
    next_owner: str
    resume_check: str


SCENARIOS = [
    HandoffCase(
        name="Repeat the story",
        current_goal="missing",
        state="unclear",
        actions_taken="unknown",
        open_risk="unclear",
        next_owner="unclear",
        resume_check="missing",
    ),
    HandoffCase(
        name="Duplicate charge waiting on approval",
        current_goal="resolve the duplicate charge without sending a refund twice",
        state="one refund request is pending; no second refund was sent",
        actions_taken="checked order history and attached the billing policy note",
        open_risk="payment record is still waiting on approval",
        next_owner="billing support",
        resume_check="confirm the pending request before changing the payment record",
    ),
    HandoffCase(
        name="Browser workflow at a legal checkpoint",
        current_goal="finish the application without choosing an unsupported legal status",
        state="form is open; no submission is verified",
        actions_taken="saved the direct link and stopped before submit",
        open_risk="the right-to-work dropdown needs user judgment",
        next_owner="user first, agent after approval",
        resume_check="confirm the selected legal status and the attached resume",
    ),
]

REQUIRED_FIELDS = [
    "current_goal",
    "state",
    "actions_taken",
    "open_risk",
    "next_owner",
    "resume_check",
]
MISSING_VALUES = {"missing", "unknown", "unclear", ""}


def present(value):
    return value.strip().lower() not in MISSING_VALUES


def decision(case):
    data = asdict(case)
    passed = [field for field in REQUIRED_FIELDS if present(data[field])]
    missing = [field for field in REQUIRED_FIELDS if field not in passed]
    if not missing:
        result = "READY_TO_HAND_OFF"
    elif len(passed) >= 3:
        result = "PARTIAL_HANDOFF_NEEDS_REPAIR"
    else:
        result = "TOO_VAGUE_TO_USE"
    return result, passed, missing


def next_step(result, missing):
    if result == "READY_TO_HAND_OFF":
        return "Pass the case to the named owner and require the resume check before acting."
    if result == "PARTIAL_HANDOFF_NEEDS_REPAIR":
        return "Fill the missing fields before the next agent acts: " + ", ".join(missing) + "."
    return "Do not make the next agent guess. Rebuild the current goal, state, action receipt, risk, owner, and resume check."


def as_json(case):
    result, passed, missing = decision(case)
    data = asdict(case)
    data.update(
        decision=result,
        passed_fields=passed,
        missing_fields=missing,
        next_step=next_step(result, missing),
    )
    return data


def report(case):
    result, passed, missing = decision(case)
    data = asdict(case)
    lines = [
        "Case:          " + case.name,
        "Decision:      " + result,
        "",
        "Current goal:  " + data["current_goal"],
        "State:         " + data["state"],
        "Actions taken: " + data["actions_taken"],
        "Open risk:     " + data["open_risk"],
        "Next owner:    " + data["next_owner"],
        "Resume check:  " + data["resume_check"],
        "",
        "Passed fields: " + (", ".join(passed) if passed else "none"),
        "Missing fields: " + (", ".join(missing) if missing else "none"),
        "Next step:     " + next_step(result, missing),
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Check whether a cross-agent handoff preserves current state.")
    parser.add_argument("--all", action="store_true", help="Run all example cases.")
    parser.add_argument("--scenario", type=int, choices=range(1, len(SCENARIOS) + 1), metavar="N")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of text.")
    args = parser.parse_args()

    selected = SCENARIOS if args.all else [SCENARIOS[(args.scenario or 1) - 1]]
    if args.json:
        print(json.dumps([as_json(item) for item in selected], indent=2))
        return

    for index, item in enumerate(selected, 1):
        if len(selected) > 1:
            print(f"\nCase {index} of {len(selected)}")
            print("=" * 64)
        print(report(item))


if __name__ == "__main__":
    main()