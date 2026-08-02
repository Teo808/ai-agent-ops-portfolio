# Action receipt report demo

This is a small standard-library Python demo for building a receipt after a risky automation action.

The goal is simple: if a workflow sends, submits, publishes, connects, or messages from a real account, it should leave proof that the action happened under the right account and inside the allowed boundary.

## What a receipt should show

1. The expected account.
2. The visible account.
3. The intended action.
4. The allowed boundary.
5. The confirmation that was actually seen.
6. The artifact URL or page proof.
7. Any blocker.
8. The next step.

Run it with:

```bash
python demo/action_receipt_report.py --all
```

The default scenario does not verify the action. That is intentional. If the browser session times out before account proof, there is no honest way to claim that a post, DM, application, or connection request happened.

## Why this matters

A lot of automation reports fail at the last inch. They say the agent clicked a button, but they do not prove the account, the confirmation state, or the page where the result can be checked.

For AI operator, support, QA, and implementation work, the receipt is the thing that lets someone trust the handoff without rerunning the whole workflow.
