#!/usr/bin/env python
"""
Source and status handoff checklist demo.

This script scores whether an AI support or agent-workflow handoff gives the
next person enough context to continue without rebuilding the whole story.

Usage:
    python demo/source_status_handoff_checklist.py
    python demo/source_status_handoff_checklist.py --scenario 2
    python demo/source_status_handoff_checklist.py --all
    python demo/source_status_handoff_checklist.py --json
"""

import argparse
import json
from dataclasses import asdict, dataclass


@dataclass
class HandoffCase:
    name: str
    source: str
    status: str
    permission_state: str
    last_action: str
    open_work: str
    owner: str


SCENARIOS = [
    HandoffCase(
        name="Generic account note",
        source="missing",
        status="missing",
        permission_state="missing",
        last_action="unknown",
        open_work="unclear",
        owner="unclear",
    ),
    HandoffCase(
        name="Support ticket waiting on approval",
        source="billing ticket and policy note",
        status="policy current, ticket waiting on approval",
        permission_state="blocked until owner approves",
        last_action="drafted response, did not send",
        open_work="confirm approval and send after review",
        owner="support specialist",
    ),
    HandoffCase(
        name="Browser workflow stopped at checkpoint",
        source="application form and saved tracker entry",
        status="form open, submission not verified",
        permission_state="legal dropdown requires user judgment",
        last_action="saved direct link and stopped before submit",
        open_work="user selects legal status, then workflow resumes",
        owner="user first, agent after approval",
    ),
]

REQUIRED_FIELDS = [
    "source",
    "status",
    "permission_state",
    "last_action",
    "open_work",
    "owner",
]

MISSING_VALUES = {"missing", "unknown", "unclear", ""}


def present(value):
    return value.strip().lower() not in MISSING_VALUES


def score(case):
    data = asdict(case)
    passed = [field for field in REQUIRED_FIELDS if present(data[field])]
    missing = [field for field in REQUIRED_FIELDS if field not in passed]
    return passed, missing


def decision(case):
    passed, missing = score(case)
    if not missing:
        return "READY_TO_HAND_OFF", passed, missing
    if len(passed) >= 3:
        return "PARTIAL_HANDOFF_NEEDS_REPAIR", passed, missing
    return "TOO_VAGUE_TO_USE", passed, missing


def next_step(result, missing):
    if result == "READY_TO_HAND_OFF":
        return "Hand off to the named owner and keep the receipt with the case."
    if result == "PARTIAL_HANDOFF_NEEDS_REPAIR":
        return "Fill the missing fields before the next person acts: " + ", ".join(missing) + "."
    return "Do not make the next person guess. Rebuild the source, status, permission state, last action, open work, and owner."


def build_report(case):
    result, passed, missing = decision(case)
    lines = [
        "Case:     " + case.name,
        "Decision: " + result,
        "",
        "Fields:",
        "  Source:           " + case.source,
        "  Status:           " + case.status,
        "  Permission state: " + case.permission_state,
        "  Last action:      " + case.last_action,
        "  Open work:        " + case.open_work,
        "  Owner:            " + case.owner,
        "",
        "Passed fields:  " + (", ".join(passed) if passed else "none"),
        "Missing fields: " + (", ".join(missing) if missing else "none"),
        "Next step:      " + next_step(result, missing),
    ]
    return "\n".join(lines)


def as_json(case):
    result, passed, missing = decision(case)
    data = asdict(case)
    data["decision"] = result
    data["passed_fields"] = passed
    data["missing_fields"] = missing
    data["next_step"] = next_step(result, missing)
    return data


def main():
    parser = argparse.ArgumentParser(
        description="Check whether an AI support handoff has enough source and status context."
    )
    parser.add_argument("--all", action="store_true", help="Run all example cases.")
    parser.add_argument(
        "--scenario",
        type=int,
        choices=range(1, len(SCENARIOS) + 1),
        metavar="N",
        help="Run one example case.",
    )
    parser.add_argument("--json", action="store_true", help="Print JSON instead of text.")
    args = parser.parse_args()

    selected = SCENARIOS if args.all else [SCENARIOS[(args.scenario or 1) - 1]]

    if args.json:
        print(json.dumps([as_json(item) for item in selected], indent=2))
        return

    for index, item in enumerate(selected, 1):
        if len(selected) > 1:
            print("\nCase " + str(index) + " of " + str(len(selected)))
            print("=" * 64)
        print(build_report(item))


if __name__ == "__main__":
    main()
