#!/usr/bin/env python
"""
Application run gate demo.

This script turns job lead evidence into a conservative apply, stage, save, or
reject decision. It is built for actor-first job search workflows where the job
has to support auditions and class instead of taking over the week.

Usage:
    python demo/application_run_gate.py
    python demo/application_run_gate.py --scenario 2
    python demo/application_run_gate.py --all
    python demo/application_run_gate.py --json
"""

import argparse
import json
from dataclasses import asdict, dataclass


@dataclass
class LeadCheck:
    name: str
    company: str
    role: str
    pay: str
    schedule: str
    location_mode: str
    commute_minutes: int
    role_family: str
    customer_load: str
    hard_blocker: str
    browser_state: str
    portal_path: str


SCENARIOS = [
    LeadCheck(
        name="Remote AI product support with browser unavailable",
        company="Example AI tools company",
        role="Product Support Specialist",
        pay="$58,000 to $72,000",
        schedule="full time, remote, steady hours",
        location_mode="remote",
        commute_minutes=0,
        role_family="AI product support",
        customer_load="mostly written support and internal handoff",
        hard_blocker="none",
        browser_state="approved browser timed out before account proof",
        portal_path="employer job portal",
    ),
    LeadCheck(
        name="Local admin role with missing schedule",
        company="Example local office",
        role="Operations Assistant",
        pay="$22 per hour",
        schedule="unknown",
        location_mode="in person",
        commute_minutes=16,
        role_family="operations admin",
        customer_load="low",
        hard_blocker="none",
        browser_state="ready",
        portal_path="LinkedIn Easy Apply",
    ),
    LeadCheck(
        name="Commission-heavy outreach role",
        company="Example sales group",
        role="Business Development Representative",
        pay="commission only",
        schedule="full time",
        location_mode="hybrid",
        commute_minutes=22,
        role_family="sales",
        customer_load="heavy cold outreach",
        hard_blocker="commission_only",
        browser_state="ready",
        portal_path="Indeed",
    ),
    LeadCheck(
        name="Far commute with vague flexibility",
        company="Example contractor",
        role="Office Coordinator",
        pay="$23 per hour",
        schedule="full time, flexibility not stated",
        location_mode="in person",
        commute_minutes=48,
        role_family="office coordination",
        customer_load="moderate phones",
        hard_blocker="far_commute",
        browser_state="ready",
        portal_path="employer job portal",
    ),
    LeadCheck(
        name="Routine admin role with clear fit",
        company="Example operations team",
        role="Data Entry Coordinator",
        pay="$21 per hour",
        schedule="part time weekday mornings",
        location_mode="in person",
        commute_minutes=14,
        role_family="data entry and records",
        customer_load="low",
        hard_blocker="none",
        browser_state="ready",
        portal_path="employer job portal",
    ),
]


REJECT_BLOCKERS = {
    "commission_only",
    "mlm",
    "door_to_door",
    "unpaid",
    "scam_risk",
    "degree_required_not_met",
    "license_required_not_met",
}

MANUAL_BLOCKERS = {
    "captcha",
    "two_factor_login",
    "security_checkpoint",
    "legal_consent",
    "ssn_request",
    "government_id_request",
    "references_required",
    "assessment_required",
}


PRIORITY_FAMILIES = {
    "AI product support",
    "AI operations",
    "technical support",
    "implementation support",
    "operations admin",
    "data entry and records",
    "business admin",
    "workplace operations",
}


def pay_is_known(lead):
    return lead.pay.lower() not in {"", "unknown", "not listed"}


def schedule_is_clear(lead):
    schedule = lead.schedule.lower()
    return schedule not in {"", "unknown", "unclear", "not listed"}


def commute_is_ok(lead):
    if lead.location_mode == "remote":
        return True
    return lead.commute_minutes <= 25


def browser_is_ready(lead):
    return lead.browser_state == "ready"


def fits_actor_first_lane(lead):
    if lead.role_family not in PRIORITY_FAMILIES:
        return False
    if "heavy" in lead.customer_load.lower() and "support" not in lead.role_family.lower():
        return False
    return True


def decide(lead):
    reasons = []

    if lead.hard_blocker in REJECT_BLOCKERS:
        return "REJECT", ["hard exclusion: " + lead.hard_blocker]

    if lead.hard_blocker in MANUAL_BLOCKERS:
        return "MANUAL_CHECKPOINT", ["user-only checkpoint: " + lead.hard_blocker]

    if lead.hard_blocker == "far_commute" and not commute_is_ok(lead):
        return "REJECT", ["commute is too far for an acting-first support job"]

    if not pay_is_known(lead):
        reasons.append("pay is missing")

    if not schedule_is_clear(lead):
        reasons.append("schedule is unclear")

    if not commute_is_ok(lead):
        reasons.append("commute is outside the normal radius")

    if not fits_actor_first_lane(lead):
        reasons.append("role family or customer load is a weak fit")

    if reasons:
        return "SAVE_FOR_REVIEW", reasons

    if not browser_is_ready(lead):
        return "STAGE_NOT_SUBMIT", [
            "role looks usable, but the approved browser session is not verified"
        ]

    return "APPLY", [
        "pay, schedule, commute, legitimacy, and role fit pass the gate"
    ]


def next_step(lead, decision):
    if decision == "APPLY":
        return "Tailor the resume, answer routine questions truthfully, submit, capture the confirmation, then log outreach handoff."
    if decision == "STAGE_NOT_SUBMIT":
        return "Create or keep the tailored materials, restore the approved browser session, then continue from the saved portal link."
    if decision == "SAVE_FOR_REVIEW":
        return "Save the lead with the missing pay, schedule, commute, or fit detail. Do not apply until the missing detail is clear."
    if decision == "MANUAL_CHECKPOINT":
        return "Leave the application on the checkpoint page and tell the user exactly what they need to finish."
    return "Do not apply. Log the exclusion so the next run does not waste time on the same lead."


def build_report(lead):
    decision, reasons = decide(lead)
    lines = [
        "Lead:           " + lead.name,
        "Decision:       " + decision,
        "Company:        " + lead.company,
        "Role:           " + lead.role,
        "Portal path:    " + lead.portal_path,
        "",
        "Evidence:",
        "  Pay:           " + lead.pay,
        "  Schedule:      " + lead.schedule,
        "  Location mode: " + lead.location_mode,
        "  Commute:       " + str(lead.commute_minutes) + " minutes",
        "  Role family:   " + lead.role_family,
        "  Customer load: " + lead.customer_load,
        "  Hard blocker:  " + lead.hard_blocker,
        "  Browser state: " + lead.browser_state,
        "",
        "Why:",
    ]
    for reason in reasons:
        lines.append("  " + reason)
    lines += ["", "Next step:", "  " + next_step(lead, decision)]
    return "\n".join(lines)


def lead_as_json(lead):
    decision, reasons = decide(lead)
    data = asdict(lead)
    data["decision"] = decision
    data["reasons"] = reasons
    data["next_step"] = next_step(lead, decision)
    return data


def main():
    parser = argparse.ArgumentParser(
        description="Turn job lead evidence into an actor-first application decision."
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
        print(json.dumps([lead_as_json(item) for item in selected], indent=2))
        return

    for index, lead in enumerate(selected, 1):
        if len(selected) > 1:
            print("\nLead " + str(index) + " of " + str(len(selected)))
            print("=" * 64)
        print(build_report(lead))


if __name__ == "__main__":
    main()
