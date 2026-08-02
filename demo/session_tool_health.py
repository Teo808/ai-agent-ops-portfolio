#!/usr/bin/env python
"""
Session tool health demo.

This script separates two problems that often get mixed together in agent work:
whether the tool server is installed and reachable, and whether the active agent
session can actually use that tool for a real-account action.

Usage:
    python demo/session_tool_health.py
    python demo/session_tool_health.py --scenario 2
    python demo/session_tool_health.py --all
    python demo/session_tool_health.py --json
"""

import argparse
import json
from dataclasses import asdict, dataclass


@dataclass
class ToolHealthCase:
    name: str
    intended_action: str
    in_session_tool_call: str
    external_health_test: str
    real_account_required: str
    duplicate_risk: str
    safe_local_work_available: str


SCENARIOS = [
    ToolHealthCase(
        name="Active session times out, health test passes",
        intended_action="post one useful LinkedIn or X comment from a signed in career account",
        in_session_tool_call="timeout after 120 seconds",
        external_health_test="tool server connects and lists tools",
        real_account_required="yes",
        duplicate_risk="low",
        safe_local_work_available="yes",
    ),
    ToolHealthCase(
        name="Active session works and account is verified",
        intended_action="send a connection note inside an approved boundary",
        in_session_tool_call="success with visible target page",
        external_health_test="not needed",
        real_account_required="yes",
        duplicate_risk="low",
        safe_local_work_available="not needed",
    ),
    ToolHealthCase(
        name="Tool works, but the account is not verified",
        intended_action="apply to a job through a logged in portal",
        in_session_tool_call="success with unknown account",
        external_health_test="tool server connects and lists tools",
        real_account_required="yes",
        duplicate_risk="low",
        safe_local_work_available="yes",
    ),
    ToolHealthCase(
        name="Tool works, but the relationship is already warm today",
        intended_action="send another recruiter follow-up",
        in_session_tool_call="success with verified account",
        external_health_test="not needed",
        real_account_required="yes",
        duplicate_risk="high",
        safe_local_work_available="yes",
    ),
]


def session_usable(case):
    text = case.in_session_tool_call.lower()
    return text.startswith("success") and "unknown account" not in text


def health_passed(case):
    text = case.external_health_test.lower()
    return "connects" in text or text == "not needed"


def account_action_needed(case):
    return case.real_account_required.lower() == "yes"


def duplicate_risk_high(case):
    return case.duplicate_risk.lower() == "high"


def decide(case):
    reasons = []

    if duplicate_risk_high(case):
        return "WAIT_OR_FIND_NEW_TARGET", [
            "recent outreach makes another message more likely to hurt than help"
        ]

    if session_usable(case):
        return "READY_WITH_RECEIPT_REQUIRED", [
            "active session is usable for the stated account action"
        ]

    if account_action_needed(case):
        reasons.append("active session cannot prove the real account action path")

    if health_passed(case):
        reasons.append(
            "separate health test says the server exists, so refresh the active session before acting"
        )
    else:
        reasons.append("tool health is not proven")

    if case.safe_local_work_available.lower() == "yes":
        return "STOP_ACCOUNT_ACTIONS_AND_DO_SAFE_LOCAL_PROOF", reasons

    return "STOP_AND_ESCALATE", reasons


def next_step(case, decision):
    if decision == "READY_WITH_RECEIPT_REQUIRED":
        return "Take only the approved action, then capture a visible receipt."

    if decision == "WAIT_OR_FIND_NEW_TARGET":
        return "Do not nudge the same person again. Check for a new target or wait for a reply."

    if decision == "STOP_ACCOUNT_ACTIONS_AND_DO_SAFE_LOCAL_PROOF":
        return "Do not use a sandbox or copied profile. Refresh the active session, and use safe local portfolio work while waiting."

    return "Leave a short recovery note with the exact failing call and the first health check to rerun."


def build_report(case):
    decision, reasons = decide(case)
    lines = [
        "Case:            " + case.name,
        "Decision:        " + decision,
        "Intended action: " + case.intended_action,
        "",
        "Evidence:",
        "  In-session call:        " + case.in_session_tool_call,
        "  External health test:   " + case.external_health_test,
        "  Real account required:  " + case.real_account_required,
        "  Duplicate risk:         " + case.duplicate_risk,
        "  Safe local work exists: " + case.safe_local_work_available,
        "",
        "Why:",
    ]

    for reason in reasons:
        lines.append("  " + reason)

    lines += ["", "Next step:", "  " + next_step(case, decision)]
    return "\n".join(lines)


def case_as_json(case):
    decision, reasons = decide(case)
    data = asdict(case)
    data["decision"] = decision
    data["reasons"] = reasons
    data["next_step"] = next_step(case, decision)
    return data


def main():
    parser = argparse.ArgumentParser(
        description="Decide whether a tool failure is safe to act through, should wait, or should become local proof."
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
        print(json.dumps([case_as_json(item) for item in selected], indent=2))
        return

    for index, case in enumerate(selected, 1):
        if len(selected) > 1:
            print("\nCase " + str(index) + " of " + str(len(selected)))
            print("=" * 64)
        print(build_report(case))


if __name__ == "__main__":
    main()
