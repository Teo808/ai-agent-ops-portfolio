#!/usr/bin/env python
"""
Action receipt report demo.

This script turns a risky automation action into a short receipt. It is meant
for job applications, recruiter outreach, social comments, and account work
where "I clicked it" is not enough proof.

Usage:
    python demo/action_receipt_report.py
    python demo/action_receipt_report.py --scenario 2
    python demo/action_receipt_report.py --all
    python demo/action_receipt_report.py --json
"""

import argparse
import json
from dataclasses import asdict, dataclass


@dataclass
class ActionReceipt:
    name: str
    platform: str
    account_expected: str
    account_visible: str
    intended_action: str
    allowed_boundary: str
    confirmation_seen: str
    artifact_url: str
    blocker: str
    next_step: str


SCENARIOS = [
    ActionReceipt(
        name="Browser timed out before social account proof",
        platform="LinkedIn or X",
        account_expected="Matteo career account",
        account_visible="unknown",
        intended_action="post a public AI workflow QA comment",
        allowed_boundary="one public comment only after account proof",
        confirmation_seen="none",
        artifact_url="none",
        blocker="browser_attach_timeout",
        next_step="restore the verified browser session before any post, DM, or connection request",
    ),
    ActionReceipt(
        name="Public comment with visible confirmation",
        platform="LinkedIn",
        account_expected="Matteo career account",
        account_visible="Matteo career account",
        intended_action="publish one public comment",
        allowed_boundary="comment only, no application claim, no DM",
        confirmation_seen="comment visible under the expected name after reload",
        artifact_url="https://example.com/feed/post/123",
        blocker="none",
        next_step="log the exact text and recheck only if someone replies",
    ),
    ActionReceipt(
        name="Application staged but blocked at user consent",
        platform="Employer portal",
        account_expected="candidate account",
        account_visible="candidate account",
        intended_action="submit a job application",
        allowed_boundary="upload resume and draft answers, but stop at legal consent",
        confirmation_seen="resume attached, submit not clicked",
        artifact_url="https://example.com/jobs/apply/123",
        blocker="legal_consent",
        next_step="leave the tab staged and ask the user to review the consent",
    ),
]


STOP_BLOCKERS = {
    "browser_attach_timeout",
    "unknown_account",
    "captcha",
    "two_factor_login",
    "security_checkpoint",
    "legal_consent",
    "payment_request",
    "sensitive_personal_data",
}


def account_verified(receipt):
    return receipt.account_visible == receipt.account_expected


def confirmation_verified(receipt):
    missing = {"", "none", "unknown", "unverified"}
    return receipt.confirmation_seen.lower() not in missing


def artifact_verified(receipt):
    missing = {"", "none", "unknown", "unverified"}
    return receipt.artifact_url.lower() not in missing


def status(receipt):
    reasons = []

    if not account_verified(receipt):
        reasons.append("expected account was not verified")

    if receipt.blocker in STOP_BLOCKERS:
        reasons.append("stop blocker present: " + receipt.blocker)

    if not confirmation_verified(receipt):
        reasons.append("visible confirmation is missing")

    if not artifact_verified(receipt):
        reasons.append("artifact URL or page proof is missing")

    if reasons:
        return "NOT VERIFIED", reasons

    return "VERIFIED", ["account, boundary, confirmation, and artifact proof are present"]


def build_report(receipt):
    result, reasons = status(receipt)
    lines = [
        "Receipt:        " + receipt.name,
        "Platform:       " + receipt.platform,
        "Status:         " + result,
        "Intended action:" + " " + receipt.intended_action,
        "Boundary:       " + receipt.allowed_boundary,
        "",
        "Evidence:",
        "  Expected account: " + receipt.account_expected,
        "  Visible account:  " + receipt.account_visible,
        "  Confirmation:     " + receipt.confirmation_seen,
        "  Artifact URL:      " + receipt.artifact_url,
        "  Blocker:           " + receipt.blocker,
        "",
        "Why:",
    ]

    for reason in reasons:
        lines.append("  " + reason)

    lines += ["", "Next step:", "  " + receipt.next_step]
    return "\n".join(lines)


def receipt_as_json(receipt):
    result, reasons = status(receipt)
    data = asdict(receipt)
    data["status"] = result
    data["reasons"] = reasons
    return data


def main():
    parser = argparse.ArgumentParser(
        description="Build a short verification receipt for risky automation actions."
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
        print(json.dumps([receipt_as_json(item) for item in selected], indent=2))
        return

    for index, receipt in enumerate(selected, 1):
        if len(selected) > 1:
            print("\nReceipt " + str(index) + " of " + str(len(selected)))
            print("=" * 64)
        print(build_report(receipt))


if __name__ == "__main__":
    main()
