# Browser attach health check demo

This is a small standard-library Python demo for deciding whether a real-account browser workflow can continue.

The problem it covers is common in agent work: the browser tool may be installed, but that does not prove the extension is attached, the right tab is selected, the expected account is visible, or the action is safe.

## What the check asks

1. Did the Playwright extension return a usable tab list?
2. Is the target page visible?
3. Is the expected account visible?
4. Is there a hard stop blocker like CAPTCHA, two factor login, encrypted message passcode, legal consent, or sensitive personal data?
5. Is any fallback allowed under the user's rules?
6. What should the next run check first?

Run it with:

```bash
python demo/browser_attach_health_check.py --all
```

## Why this matters

For social outreach, recruiter messages, and job applications, a browser attach failure is not a small technical detail. It changes what the agent is allowed to do.

If the extension times out before account proof, the right answer is to stop and report the blocker. If the extension is connected but only shows the welcome tab, the next step is different: open the target site in the same verified browser session, then check the account before acting.

That distinction protects the user and makes the handoff useful for the next operator or agent run.
