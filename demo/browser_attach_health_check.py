#!/usr/bin/env python
"""
Browser attach health check demo.

This script turns browser-control evidence into a short operator decision. It is
for career social, job applications, and other real-account workflows where the
agent must know whether the browser is actually controllable before it acts.

Usage:
    python demo/browser_attach_health_check.py
    python demo/browser_attach_health_check.py --scenario 2
    python demo/browser_attach_health_check.py --all
    python demo/browser_attach_health_check.py --json
"""

import argparse
import json
from dataclasses import asdict, dataclass


@dataclass
class AttachCheck:
    name: str
    expected_browser: str
    tabs_call: str
    visible_target: str
    expected_account: str
    visible_account: str
    safety_blocker: str
    intended_action: str
    fallback_allowed: str


SCENARIOS = [
    AttachCheck(
        name="Extension times out before any tab list",
        expected_browser="Matteo Chrome through the Playwright extension",
        tabs_call="timeout after 120 seconds",
        visible_target="unknown",
        expected_account="Matteo career account",
        visible_account="unknown",
        safety_blocker="browser_attach_timeout",
        intended_action="check notifications and post one AI workflow QA comment",
        fallback_allowed="no",
    ),
    AttachCheck(
        name="Extension connected on the welcome tab only",
        expected_browser="Matteo Chrome through the Playwright extension",
        tabs_call="success",
        visible_target="Playwright extension welcome tab",
        expected_account="Matteo career account",
        visible_account="unknown",
        safety_blocker="no_target_tab",
        intended_action="open LinkedIn or X in the same verified browser window",
        fallback_allowed="yes, same extension session only",
    ),
    AttachCheck(
        name="LinkedIn account verified and no blocker",
        expected_browser="Matteo Chrome through the Playwright extension",
        tabs_call="success",
        visible_target="LinkedIn feed",
        expected_account="Matteo career account",
        visible_account="Matteo career account",
        safety_blocker="none",
        intended_action="write one public comment inside the stated boundary",
        fallback_allowed="not needed",
    ),
    AttachCheck(
        name="X asks for encrypted message passcode",
        expected_browser="Matteo Chrome through the Playwright extension",
        tabs_call="success",
        visible_target="X direct message composer",
        expected_account="Scythe career account",
        visible_account="Scythe career account",
        safety_blocker="encrypted_message_passcode",
        intended_action="send a private X DM",
        fallback_allowed="no",
    ),
]


HARD_STOP_BLOCKERS = {
    "browser_attach_timeout",
    "unknown_account",
    "captcha",
    "two_factor_login",
    "security_checkpoint",
    "encrypted_message_passcode",
    "payment_request",
    "legal_consent",
    "sensitive_personal_data",
}


def tabs_connected(check):
    return check.tabs_call.lower() == "success"


def target_verified(check):
    missing = {"", "unknown", "about:blank"}
    return check.visible_target.lower() not in missing


def account_verified(check):
    return check.visible_account == check.expected_account


def decide(check):
    reasons = []

    if not tabs_connected(check):
        reasons.append("Playwright extension did not return a usable tab list")

    if not target_verified(check):
        reasons.append("target page was not verified")

    if not account_verified(check):
        reasons.append("expected account was not verified")

    if check.safety_blocker in HARD_STOP_BLOCKERS:
        reasons.append("hard stop blocker present: " + check.safety_blocker)

    if reasons:
        if check.safety_blocker == "no_target_tab" and tabs_connected(check):
            return "OPEN_TARGET_IN_VERIFIED_BROWSER", [
                "extension is reachable, but the target account page is not selected yet"
            ]
        return "STOP", reasons

    return "READY_INSIDE_BOUNDARY", [
        "browser, target, account, and blocker state are usable"
    ]


def next_step(check, decision):
    if decision == "READY_INSIDE_BOUNDARY":
        return "Take only the intended action, then capture a visible receipt."

    if decision == "OPEN_TARGET_IN_VERIFIED_BROWSER":
        return "Open the target site through the same extension session, then verify the visible account before acting."

    if check.safety_blocker == "browser_attach_timeout":
        return "Do not use sandbox or copied browsers. Restore the extension connection before any send, post, DM, follow, or application action."

    if check.safety_blocker == "encrypted_message_passcode":
        return "Do not send the DM. Use a public reply, LinkedIn path, or save the target for manual follow-up."

    return "Leave a short recovery note with the exact blocker and first check for the next run."


def build_report(check):
    decision, reasons = decide(check)
    lines = [
        "Check:          " + check.name,
        "Decision:       " + decision,
        "Expected browser:" + " " + check.expected_browser,
        "Intended action:" + " " + check.intended_action,
        "Fallback allowed:" + " " + check.fallback_allowed,
        "",
        "Evidence:",
        "  Tabs call:        " + check.tabs_call,
        "  Visible target:   " + check.visible_target,
        "  Expected account: " + check.expected_account,
        "  Visible account:  " + check.visible_account,
        "  Safety blocker:   " + check.safety_blocker,
        "",
        "Why:",
    ]

    for reason in reasons:
        lines.append("  " + reason)

    lines += ["", "Next step:", "  " + next_step(check, decision)]
    return "\n".join(lines)


def check_as_json(check):
    decision, reasons = decide(check)
    data = asdict(check)
    data["decision"] = decision
    data["reasons"] = reasons
    data["next_step"] = next_step(check, decision)
    return data


def main():
    parser = argparse.ArgumentParser(
        description="Turn browser attachment evidence into an operator decision."
    )
    parser.add_argument("--all", action="store_true", help="Run all example checks.")
    parser.add_argument(
        "--scenario",
        type=int,
        choices=range(1, len(SCENARIOS) + 1),
        metavar="N",
        help="Run one example check.",
    )
    parser.add_argument("--json", action="store_true", help="Print JSON instead of text.")
    args = parser.parse_args()

    selected = SCENARIOS if args.all else [SCENARIOS[(args.scenario or 1) - 1]]

    if args.json:
        print(json.dumps([check_as_json(item) for item in selected], indent=2))
        return

    for index, check in enumerate(selected, 1):
        if len(selected) > 1:
            print("\nCheck " + str(index) + " of " + str(len(selected)))
            print("=" * 64)
        print(build_report(check))


if __name__ == "__main__":
    main()
