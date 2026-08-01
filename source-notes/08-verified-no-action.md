# Verified no-action rule

Sometimes the safest automation result is a clean no-action report.

If an agent cannot prove the browser session, account, action boundary, or final result, it should stop before the click. That is not a failed run. It is the point where the workflow protects the user.

## When to stop

Stop when the agent cannot verify one of these:

- The controlled browser is the real target session
- The visible account is the expected account
- The next click is inside the approved action boundary
- The page does not show CAPTCHA, two factor login, legal consent, payment, SSN, government ID, or another user-only checkpoint
- The result can be checked after the action

If any of those are missing, the honest status is not verified.

## What the report should say

A useful no-action report should be short and specific.

Include:

1. What the agent tried
2. The exact proof it could not get
3. What it did not do because of that missing proof
4. What the next run should check first
5. Whether any files, drafts, tabs, or messages were changed

Example:

The agent tried to open the social account through the approved browser path. The browser control layer timed out before the LinkedIn or X account could be verified. No post, DM, comment, follow, application, or email was sent. The next run should start by checking browser tabs through the approved session, then verify the target account before any outbound action.

## Why this matters

Automation gets dangerous when it treats partial access like proof.

For job applications, recruiter outreach, social posts, and ecommerce work, a guessed action can create cleanup work or make the user look careless. A verified no-action report is better than a fake success claim.

This is the operator habit I want to keep building: act when the proof is there, stop when it is not, and leave enough state for the next person to continue cleanly.
