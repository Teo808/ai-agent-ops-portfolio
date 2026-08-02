#!/usr/bin/env python
"""
Real-account automation incident runbook demo.

This script turns a browser or automation failure into a safe account-action
plan. It is meant for workflows where the next click would post, DM, apply,
upload, submit, follow, or message from a real account.

Usage:
    python demo/real_account_incident_runbook.py
    python demo/real_account_incident_runbook.py --scenario 2
    python demo/real_account_incident_runbook.py --all
    python demo/real_account_incident_runbook.py --json
"""

import argparse
import json
from dataclasses import asdict, dataclass


@dataclass
class IncidentCase:
    name: str
    intended_action: str
    active_session: str
    account_proof: str
    boundary_proof: str
    result_proof_path: str
    duplicate_contact_risk: str
    safe_local_work: str


SCENARIOS = [
    IncidentCase(
        name="Browser tool timeout before social action",
        intended_action="post one useful AI workflow QA comment from a signed in account",
        active_session="tab call timed out before target page opened",
        account_proof="missing",
        boundary_proof="missing",
        result_proof_path="missing",
        duplicate_contact_risk="low",
        safe_local_work="portfolio runbook available",
    ),
    IncidentCase(
        name="Verified browser with clear target",
        intended_action="send one approved recruiter follow-up",
        active_session="target page visible and usable",
        account_proof="verified",
        boundary_proof="approved action only",
        result_proof_path="visible sent confirmation available",
        duplicate_contact_risk="low",
        safe_local_work="not needed",
    ),
    IncidentCase(
        name="Tool server healthy but account unknown",
        intended_action="submit a job application from a portal",
        active_session="tool server lists tools in a separate test",
        account_proof="unknown",
        boundary_proof="job link known",
        result_proof_path="confirmation page expected",
        duplicate_contact_risk="low",
        safe_local_work="tailored materials available",
    ),
    IncidentCase(
        name="Recovered browser but same contact already touched",
        intended_action="send another message to the same recruiter",
        active_session="target page visible and usable",
        account_proof="verified",
        boundary_proof="approved action only",
        result_proof_path="visible sent confirmation available",
        duplicate_contact_risk="high",
        safe_local_work="new target research available",
    ),
]


def has_active_session(case):
    return case.active_session == "target page visible and usable"


def has_account_proof(case):
    return case.account_proof == "verified"


def has_boundary(case):
    return case.boundary_proof == "approved action only"


def has_result_path(case):
    return "confirmation" in case.result_proof_path or "sent confirmation" in case.result_proof_path


def duplicate_risk_high(case):
    return case.duplicate_contact_risk == "high"


def decide(case):
    reasons = []

    if duplicate_risk_high(case):
        return "WAIT_OR_FIND_NEW_TARGET", [
            "recent contact history makes another message lower value"
        ]

    if has_active_session(case) and has_account_proof(case) and has_boundary(case) and has_result_path(case):
        return "READY_WITH_RECEIPT_REQUIRED", [
            "browser, account, boundary, and receipt path are all proven"
        ]

    if not has_active_session(case):
        reasons.append("active browser session is not proven")
    if not has_account_proof(case):
        reasons.append("account proof is missing or unknown")
    if not has_boundary(case):
        reasons.append("approved action boundary is not proven")
    if not has_result_path(case):
        reasons.append("result proof path is missing")

    if case.safe_local_work != "not needed":
        return "BLOCK_REAL_ACCOUNT_ACTIONS_AND_DO_LOCAL_PROOF", reasons

    return "STOP_AND_ESCALATE", reasons


def next_step(case, decision):
    if decision == "READY_WITH_RECEIPT_REQUIRED":
        return "Take only the approved action, then capture the visible receipt and log it."
    if decision == "WAIT_OR_FIND_NEW_TARGET":
        return "Do not message the same contact again. Wait for a reply or find a different safe target."
    if decision == "BLOCK_REAL_ACCOUNT_ACTIONS_AND_DO_LOCAL_PROOF":
        return "Do not use a sandbox or guessed account. Save the draft, build safe local proof, and repair the verified browser path."
    return "Leave an incident note with the exact failure and the first repair check."


def build_report(case):
    decision, reasons = decide(case)
    lines = [
        "Case:            " + case.name,
        "Decision:        " + decision,
        "Intended action: " + case.intended_action,
        "",
        "Evidence:",
        "  Active session:         " + case.active_session,
        "  Account proof:          " + case.account_proof,
        "  Boundary proof:         " + case.boundary_proof,
        "  Result proof path:      " + case.result_proof_path,
        "  Duplicate contact risk: " + case.duplicate_contact_risk,
        "  Safe local work:        " + case.safe_local_work,
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
        description="Turn a real-account automation incident into a safe action plan."
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
