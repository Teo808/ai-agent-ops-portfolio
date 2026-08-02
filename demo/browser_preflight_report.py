#!/usr/bin/env python3
"""
Browser preflight report demo.

This small script turns browser automation evidence into a send or stop decision.
It is meant for social posts, recruiter messages, job applications, and other
real-account workflows where a bad click matters.

Usage:
    python demo/browser_preflight_report.py
    python demo/browser_preflight_report.py --scenario 2
    python demo/browser_preflight_report.py --all
    python demo/browser_preflight_report.py --json
"""

import argparse
import json
from dataclasses import dataclass, asdict


STOP_BLOCKERS = {
    "captcha",
    "two_factor_login",
    "security_checkpoint",
    "legal_consent",
    "sensitive_personal_data",
    "payment_request",
    "assessment",
    "unknown_account",
}


@dataclass
class BrowserScenario:
    name: str
    target: str
    url: str
    title: str
    expected_account: str
    visible_account: str
    action_boundary: str
    intended_action: str
    blocker: str
    result_proof: str


SCENARIOS = [
    BrowserScenario(
        name="Extension preflight times out before account proof",
        target="Career social comment",
        url="unverified",
        title="unverified",
        expected_account="known personal career account",
        visible_account="unknown",
        action_boundary="comment only after account proof",
        intended_action="post a public reply about AI workflow QA",
        blocker="unknown_account",
        result_proof="none",
    ),
    BrowserScenario(
        name="Signed-in page with a clean comment boundary",
        target="AI tooling post",
        url="https://example.com/feed/post/123",
        title="AI tooling discussion",
        expected_account="known personal career account",
        visible_account="known personal career account",
        action_boundary="one public comment, no DM, no application claim",
        intended_action="publish one short public comment",
        blocker="none",
        result_proof="comment visible under the expected account after reload",
    ),
    BrowserScenario(
        name="Application form reaches legal consent",
        target="Job portal submit flow",
        url="https://example.com/jobs/apply",
        title="Application form",
        expected_account="candidate account",
        visible_account="candidate account",
        action_boundary="upload and draft allowed, legal consent requires user",
        intended_action="submit application",
        blocker="legal_consent",
        result_proof="resume attached, submit not clicked",
    ),
]


def has_context_proof(scenario):
    missing = {"", "unknown", "unverified", "none"}
    return scenario.url.lower() not in missing and scenario.title.lower() not in missing


def has_account_proof(scenario):
    return (
        scenario.visible_account
        and scenario.visible_account.lower() != "unknown"
        and scenario.visible_account == scenario.expected_account
    )


def has_result_proof(scenario):
    return scenario.result_proof.lower() not in {"", "none", "unverified"}


def decide(scenario):
    reasons = []

    if not has_context_proof(scenario):
        reasons.append("browser context was not verified")

    if not has_account_proof(scenario):
        reasons.append("expected account was not verified")

    if scenario.blocker in STOP_BLOCKERS:
        reasons.append("stop blocker present: " + scenario.blocker)

    if not reasons and "submit" in scenario.intended_action.lower() and not has_result_proof(scenario):
        reasons.append("submit result proof is missing")

    if reasons:
        return "STOP", reasons

    return "READY", ["context, account, boundary, blocker state, and result proof are usable"]


def next_step(decision, scenario):
    if decision == "READY":
        return "Proceed inside the stated boundary, then verify the result again after the click."

    if scenario.blocker == "unknown_account":
        return "Restore browser attachment and verify the visible account before any send, submit, or publish action."

    if scenario.blocker == "legal_consent":
        return "Leave the form staged and ask the user to review the consent before submission."

    return "Leave a recovery packet with the exact blocker and first check for the next run."


def build_report(scenario):
    decision, reasons = decide(scenario)
    lines = [
        "Scenario:       " + scenario.name,
        "Target:         " + scenario.target,
        "Decision:       " + decision,
        "Intended action:" + " " + scenario.intended_action,
        "Boundary:       " + scenario.action_boundary,
        "",
        "Evidence:",
        "  URL:             " + scenario.url,
        "  Title:           " + scenario.title,
        "  Expected account:" + " " + scenario.expected_account,
        "  Visible account: " + scenario.visible_account,
        "  Blocker:         " + scenario.blocker,
        "  Result proof:    " + scenario.result_proof,
        "",
        "Why:",
    ]

    for reason in reasons:
        lines.append("  " + reason)

    lines += ["", "Next step:", "  " + next_step(decision, scenario)]
    return "\n".join(lines)


def scenario_as_json(scenario):
    decision, reasons = decide(scenario)
    data = asdict(scenario)
    data["decision"] = decision
    data["reasons"] = reasons
    data["next_step"] = next_step(decision, scenario)
    return data


def main():
    parser = argparse.ArgumentParser(
        description="Turn browser automation evidence into a send or stop decision."
    )
    parser.add_argument("--all", action="store_true", help="Run all example scenarios.")
    parser.add_argument(
        "--scenario",
        type=int,
        choices=range(1, len(SCENARIOS) + 1),
        metavar="N",
        help="Run one example scenario.",
    )
    parser.add_argument("--json", action="store_true", help="Print JSON instead of text.")
    args = parser.parse_args()

    selected = SCENARIOS if args.all else [SCENARIOS[(args.scenario or 1) - 1]]

    if args.json:
        print(json.dumps([scenario_as_json(item) for item in selected], indent=2))
        return

    for index, scenario in enumerate(selected, 1):
        if len(selected) > 1:
            print("\nScenario " + str(index) + " of " + str(len(selected)))
            print("=" * 64)
        print(build_report(scenario))


if __name__ == "__main__":
    main()
