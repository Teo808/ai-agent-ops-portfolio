# Agent recovery packet

When an AI agent cannot finish a real workflow, it should leave the next person closer to done.

A useful handoff does not need a long transcript. It needs a small recovery packet that answers six questions.

## 1. What did the agent try?

List the main steps in plain language. Keep it short enough for a human to scan.

Example:

- Opened the application page
- Checked the task details
- Created the needed file
- Tried the normal upload path
- Tried the drop zone upload path

## 2. What changed?

Say what the agent actually changed, submitted, saved, moved, deleted, drafted, or uploaded.

If nothing changed, say that too. That protects the user from guessing.

Example:

The file was created locally, but the portal did not accept the upload. Nothing was submitted.

## 3. What is still open?

Name the unfinished pieces. Do not bury them in a vague status update.

Example:

The user still needs to upload the PDF, review the optional form section, and click Submit.

## 4. What blocked it?

Use the exact blocker. This is where support value shows up.

Good blockers:

- CAPTCHA
- Two-factor login
- Disabled upload button
- File input blocked by the browser automation layer
- Legal consent that needs the user
- Missing pay or schedule details
- Form question that cannot be answered truthfully from known facts

Bad blockers:

- "It did not work"
- "Something went wrong"
- "The site had an issue"

## 5. What should the user do next?

Give the next action as a short instruction, not a general suggestion.

Example:

Open the tab titled "Application form," upload the PDF named `Example_Role_Resume.pdf`, review the final questions, then click Submit.

## 6. What should the next agent check first?

This keeps the next run from starting over.

Example:

First check whether the confirmation page is visible. If not, check whether the file is still attached. Do not recreate the file unless the source changed.

## Why this matters

A failed workflow is not automatically wasted work. It becomes wasted work when the handoff is unclear.

For support, QA, operations, and implementation work, the recovery packet is the difference between a clean continuation and a mystery someone else has to untangle.

The simple standard is this: if the agent stops, the next person should know what happened, what changed, what is blocked, and where to continue.
