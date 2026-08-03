# Real-account automation incident runbook

This is a one-page runbook for a common agent operations problem: the workflow is about to touch a real account, but the active browser or automation session is not proven safe.

That matters for posts, DMs, job applications, recruiter messages, uploads, and submit buttons. A separate tool health check can help with repair, but it does not prove the current account action is safe.

## The runbook

1. State what failed. Name the exact tool call, page, account proof, or confirmation step that failed.
2. Scope what is blocked. Block sends, posts, follows, applications, uploads, and messages until verification returns.
3. Keep the evidence small. Log the exact error, last safe page, visible account proof status, and duplicate-contact risk.
4. Choose the safe decision. Stop, stage, save, or continue only with local proof work that does not touch the account.
5. Give the repair path. Reload the browser tool, start a fresh session, or restart the gateway, then verify the target account before acting.
6. Resume carefully. Check recent outreach and application history before sending anything from the recovered session.

## Example

| Evidence | Status | Decision |
| --- | --- | --- |
| Browser tab call timed out before account proof | Active session not verified | Block LinkedIn, X, job portal, and email account actions |
| Separate health test can list tools | Repair clue only | Do not treat this as permission to post or submit |
| Latest application target already received outreach | Duplicate-contact risk exists | Wait, or find a new safe target after verification returns |
| Local portfolio work is available | Safe fallback | Create proof, save a draft, and log the blocker honestly |

## Resume checklist

1. Open the recovered browser in the same real account path, not a sandbox or copied session.
2. Verify the target page, visible account, and allowed action before clicking anything public.
3. Check the latest application, message, and comment history so the workflow does not double-contact someone.
4. Take one small action first, then capture the visible receipt before doing the next one.

## Why this matters

Good agent work is not only about recovery. It is also about knowing what not to do. If the session cannot prove the browser, account, action boundary, and result path, the honest decision is to stop account actions and leave a clear handoff.

That protects the user, the account, and the relationship. It also gives the next run something concrete to check first.

Run the small demo with:

```bash
python demo/real_account_incident_runbook.py --all
```
