# AGENTS.md — Web Lab

Instructions for the OpenCode agent. This file is a short operating summary.
Full rules are in CLAUDE.md. If the two disagree, CLAUDE.md wins.

## 1. At the start of every session

1. Read CLAUDE.md.
2. Read DEVELOPMENT_PLAN.md: current phase, verified steps, open decisions.
3. Check which machine you are on (`hostname`, `uname -m`). The Raspberry Pi (`pi5home`, ARM64) is the execution server. The Ubuntu PC is the secondary development machine.
4. Inspect the repository before changing anything.
5. State the current phase and your plan in a few lines, then wait for approval if the plan needs it.

## 2. Project in one paragraph

Web Lab is an AI-assisted lab with two independent modules, website development and website parsing, sharing browser infrastructure (Firefox, Playwright, VNC). It is a DEV and testing environment with no live data. Python first, plain HTML/CSS/vanilla JavaScript for the frontend. First parsing target: Avito.ru.

## 3. Approval is required before

- Installing or removing system packages.
- Changing system configuration, systemd services, firewall, network interfaces or VPN routing.
- Changing permissions outside the project.
- Deleting files or databases.
- Changing or restarting a persistent browser profile.
- Deploying anything.
- Creating project files (ask first, then create only what was approved).

You may without asking: read files and logs, inspect configuration, write proposed code in your reply, run non-destructive project tests, and produce plans.

Do not assume root. Do not get around an approval requirement with another command, a script, or indirect execution. If a command would need approval, ask.

## 4. Hard rules

- Never commit secrets, cookies, browser profiles, logs, collected data or backups. Check `.gitignore` before the first commit.
- Never invent installed versions, network settings, credentials, API availability, quotas or test results. If you do not know, check or ask.
- Keep verified facts and hypotheses clearly separate. "Written" is not "tested". "Worked once" is not "reliable".
- Do not add dependencies, frameworks or services without a concrete reason. No React, Vue or Angular. No new browser engine before the Firefox experiments are done.
- Do not rewrite working code because another style looks cleaner.
- The Pi runs from a microSD card: avoid heavy logging, large screenshot sets and continuous traces.

## 5. Working method

1. Build the smallest experiment that proves the thing works.
2. Make small changes. Test each one.
3. When something fails: capture the error, read the logs, reproduce it, find the responsible component, try a minimal fix. Do not start by rewriting.
4. Keep modules separate. A parsing failure must not stop development work, and a development restart must not kill the parsing browser.

## 6. Browser rules

- One persistent profile per website. Never create a fresh profile per task.
- Never open the same profile in two Firefox processes.
- Leave the browser open after a task. Do not clear cookies or storage. Shutdown is an explicit operation.
- When login, a CAPTCHA or another interactive challenge appears: stop, save the task state, notify the user, and wait for them to act through VNC. Resume without losing the session.

## 7. Parsing rules

- Check whether plain HTTP is enough before reaching for the browser.
- Store only the fields defined in the extraction schema. Do not save full raw pages or snapshots. Delete debugging copies afterwards.
- Do not bypass access controls, solve CAPTCHAs automatically, impersonate users or ignore rate limits. If access is denied or limited, stop and report.
- Validate results: required fields, duplicates, pagination completeness, timestamps and source URLs. A successful HTTP response is not a successful parse.

## 8. Development rules

- Python backend, HTML templates, vanilla JavaScript, CSS. Pick the backend framework only after a small comparison.
- Inspect the existing site (HTML, CSS, JS, screenshots) before reproducing or changing a design.
- Run the app and test it in a real browser. Compare screenshots when reproducing a design.

## 9. When you finish a task, report

1. Files changed.
2. What you ran and the actual results.
3. Known limitations and anything untested.
4. DEVELOPMENT_PLAN.md updates (mark only what was verified).
5. The next logical step.

## 10. When uncertain

Stop and ask the user. One clear question is better than a wrong assumption.
