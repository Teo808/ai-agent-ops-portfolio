# Browser automation preflight checklist

Browser automation is only useful when it is acting in the right account, on the right page, with a clear idea of what it is allowed to change.

This checklist is for agent workflows that touch signed in sites, job portals, social accounts, ecommerce tools, or any page where a click can create a real result.

## 1. Confirm the browser context

Before the agent clicks anything important, it should prove which browser context it controls.

Check:

- The visible site URL
- The page title
- The account name or profile signal shown on the page
- Whether the session is signed in or sitting at a login screen
- Whether the page is a real target tab, not an extension welcome page or blank tab

If the agent cannot prove the context, it should stop and say so. It should not move to a backup browser and pretend it used the real account.

## 2. Confirm the account

For logged in workflows, the account matters as much as the URL.

Good proof:

- The profile menu shows the expected name or email
- The page shows the expected workspace, store, inbox, or candidate profile
- A recent known tab or notification confirms the same account

Weak proof:

- A Chrome process exists
- A launch command exited with code 0
- A tab opened somewhere
- Cookies seem present but the page still asks for login

The agent should record the proof it used. If it cannot verify the account, it should leave the page untouched.

## 3. Confirm the action boundary

The agent should know what it is allowed to do before it reaches the dangerous click.

Examples:

- Draft is allowed, but publish is not allowed
- Upload is allowed, but submit is not allowed after a legal consent screen
- Apply is allowed only when pay, schedule, commute, legitimacy, and fit are clear
- Comment is allowed only when the comment is specific and safe
- Email is allowed only through the configured account and a legitimate public contact path

If the next click crosses the boundary, the agent should stop with a recovery packet.

## 4. Check for real blockers

A real blocker is not the same as friction.

Normal friction:

- A stale element
- A slow page
- A failed first upload attempt
- A button that needs scrolling into view
- A form question that can be answered truthfully from known facts

Stop blockers:

- CAPTCHA
- Two factor login
- Security checkpoint
- Government ID or SSN request
- Bank or payment information request
- Legal consent that needs the user
- References with private contact details
- Assessment, video interview, or personality test
- A question where every answer would misrepresent the user

The agent should try safe alternatives for normal friction. It should not push through stop blockers.

## 5. Verify the result

After the action, the agent should prove what happened.

For a submitted form, look for a confirmation page, confirmation text, email receipt, or portal status.

For a post or comment, reopen the permalink or activity page and find the exact text under the right account.

For an upload, check that the file name or success message is visible before continuing.

If the result cannot be verified, the report should say "unverified" instead of turning a guess into a claim.

## 6. Leave a clean handoff

If the workflow stops, the next person should not have to reconstruct the whole story.

The handoff should include:

- What the agent tried
- What changed
- What is still open
- The exact blocker
- The page or tab to continue from
- What the next run should check first

That is the difference between automation that saves time and automation that creates a second mess for someone to clean up.
