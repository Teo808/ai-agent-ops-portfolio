# Browser preflight decision demo

This is a small standard-library Python demo for deciding whether a browser automation workflow should send, submit, publish, or stop.

The point is simple: before an agent acts in a real account, it should be able to prove five things.

1. The browser context is known.
2. The expected account is visible.
3. The action boundary is clear.
4. No stop blocker is present.
5. The result can be verified after the click.

If one of those is missing, the right answer is usually not another click. The right answer is a clean stop report with the first check for the next run.

## What the demo covers

The script has three example scenarios:

- A social comment where the browser extension times out before account proof.
- A signed-in page where one public comment is inside the boundary.
- A job application flow that reaches a legal consent step and must stop for the user.

Run it with:

```bash
python demo/browser_preflight_report.py --all
```

The default scenario intentionally stops. That is the behavior I want from safe automation when the account cannot be verified.

## Why this matters

A lot of agent failures are not dramatic. They are boring state problems: the wrong tab, an unknown account, a missing confirmation, or a form step that crossed from routine work into user judgment.

For support, QA, implementation, and AI operator work, catching that line matters. It protects the user and gives the next person a report they can continue from.
