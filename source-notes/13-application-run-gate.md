# Application run gate demo

This is a small standard-library Python demo for deciding whether a job lead should be applied to, staged, saved, or rejected.

The goal is actor-first job search. The job should support acting time, not swallow it. A lead only moves to apply when pay, schedule, commute, legitimacy, and role fit are clear enough.

## What the gate checks

1. Is the role in a useful lane like AI product support, AI operations, technical support, implementation support, admin operations, or data and records work?
2. Is pay known and strong enough to beat the current baseline or justify the time?
3. Is the schedule clear enough to protect auditions, self tapes, class, and acting work?
4. Is the commute reasonable for the home base, unless the role is remote or truly hybrid?
5. Is there a hard exclusion like commission-only sales, MLM, unpaid work, a required license, or a degree gate that is not met?
6. Is the approved browser session verified before any submit, send, post, DM, or account action?

Run it with:

```bash
python demo/application_run_gate.py --all
```

## Why this matters

A job agent should not apply just because a role sounds possible. It should know when to move fast and when to stop.

The useful decisions are simple:

- Apply when the lead is clear and the browser/account path is verified.
- Stage when the role fits but the approved browser path is not verified.
- Save when pay, schedule, commute, or fit needs review.
- Reject when there is a hard blocker.

That keeps the workflow honest and protects both the acting calendar and the user's real accounts.
