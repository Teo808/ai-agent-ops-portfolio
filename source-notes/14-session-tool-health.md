# Session tool health demo

This is a small standard-library Python demo for a common agent operations problem: a tool server can be installed and healthy while the active agent session still cannot use it safely.

That distinction matters when the action touches a real account. If the in-session browser tool times out before proving the page and account, the workflow should not post, DM, apply, follow, or claim success. A separate health check can explain what to fix next, but it does not prove the current action is safe.

## What the demo checks

1. Did the active session tool call return a usable page?
2. Did a separate health test prove that the server exists?
3. Does the intended action require a real signed in account?
4. Is there duplicate outreach risk?
5. Is there safe local proof work to do while the account action is blocked?

Run it with:

```bash
python demo/session_tool_health.py --all
```

## Why this matters

Good agent work needs more than a tool list. It needs proof that the current session can act in the right browser, as the right account, inside the approved boundary.

If that proof is missing, the honest move is to stop account actions, log the exact blocker, and do safe work that does not touch the account. That keeps the workflow useful without pretending a risky click happened.
