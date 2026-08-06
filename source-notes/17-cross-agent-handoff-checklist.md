# Cross-agent handoff checklist

When one agent hands a live support or workflow case to another, the next agent should not start by asking the customer to tell the whole story again.

The handoff needs enough current state to continue safely. It should not copy a full transcript just because the transcript exists.

## The checklist

1. Current goal: What is the user trying to get done now?
2. State: What has already happened, and what is the current status?
3. Actions taken: What did the previous agent read, change, or send?
4. Open risk: What could be wrong, stale, blocked, or unsafe to assume?
5. Next owner: Which person or system owns the next step?
6. Resume check: What should the next agent verify before acting?

## Example

| Handoff field | Weak handoff | Better handoff |
| --- | --- | --- |
| Current goal | "Help with the account" | "Resolve the duplicate charge without sending a refund twice" |
| State | "Issue is being handled" | "One refund request is pending. No second refund was sent." |
| Actions taken | "Checked the order" | "Checked the order history and attached the billing policy note" |
| Open risk | "Nothing major" | "The payment record is still waiting on approval" |
| Next owner | "Someone from support" | "Billing support owns the approval step" |
| Resume check | "Continue from here" | "Confirm the pending request before changing the payment record" |

## Why this matters

Shared context is useful only when it is current and easy to verify. A clean handoff gives the next agent a starting point, a boundary, and a clear reason to pause when the state is uncertain.

That applies to customer support, implementation work, browser automation, and any workflow that moves between tools or agents.

Run the small demo with:

```bash
python demo/cross_agent_handoff_checklist.py --all
```