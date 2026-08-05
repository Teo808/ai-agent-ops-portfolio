# Source and status handoff checklist

This is a small checklist for AI support and agent workflows where the answer is not useful unless the next person can trust where it came from.

More context is not automatically better. If an agent pulls history from five tools but cannot show the source, current status, permission state, or next owner, support still has to audit the whole story.

## The checklist

1. Source: What tool, policy, document, ticket, message, or record did the agent use?
2. Status: Is that source current, stale, blocked, missing, or waiting for approval?
3. Permission state: Was the agent allowed to act, asked to pause, or blocked by a real checkpoint?
4. Last action: What changed, if anything?
5. Open work: What still needs a human or the next run?
6. Owner: Who should check the next step?

## Example

| Handoff field | Weak handoff | Better handoff |
| --- | --- | --- |
| Source | "I checked the account." | "Checked the billing ticket and the latest policy note." |
| Status | "Looks good." | "Policy note is current. Billing ticket is still waiting on approval." |
| Permission | "Could not continue." | "Stopped because the action needed legal or account owner approval." |
| Next owner | "User should review." | "Support should confirm approval, then resume from the billing step." |

## Why I care about this

This is the support side of AI workflow QA. A clean handoff should reduce mystery. It should tell the next person what the agent used, what state the work is in, and what should happen next.

That habit matters for customer support, implementation, job application workflows, browser automation, and any product where an agent acts across real systems.

Run the small demo with:

```bash
python demo/source_status_handoff_checklist.py --all
```
