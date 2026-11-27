# Avito access: profile session flag and human recovery

Date: 2026-11-27
Machine: pi5home (Raspberry Pi 5, aarch64, Debian 13)
Software: Firefox ESR 153.7.0esr (system), Playwright 1.65.2 (its Firefox build 159.0), Python 3.13.5
Labels: FACT / OBSERVATION / INFERENCE / UNKNOWN

## Objective

Find why the parser stopped receiving Avito pages (HTTP 429) while the user's
own Firefox loads Avito normally, and restore access within the project rules.

## Facts

- FACT: Playwright + saved profile `~/browser-data/profiles/avito` returned
  HTTP 200 with 50 item cards on 2026-11-25 (several runs) and on 2026-11-27
  (session reuse check).
- FACT: later runs on 2026-11-27 returned HTTP 429 on the search URL
  `https://www.avito.ru/all/avtomobili?cd=1`, and the page then loaded an
  hCaptcha firewall: `POST https://www.avito.ru/web/5/firewallCaptcha/get`,
  scripts from `hcaptcha.com` and `www.avito.st/s/captcha/gt4.js`.
  Request log kept at `~/browser-data/logs/avito-search-requests.jsonl`
  (URLs and statuses only).
- FACT: three-way comparison on 2026-11-27, same machine, same IP, same time:

  | Browser                  | Profile            | Result            |
  |--------------------------|--------------------|-------------------|
  | System Firefox ESR (manual) | default        | works (normal page) |
  | Playwright Firefox (script) | avito          | 429 + hCaptcha    |
  | Playwright Firefox (script) | fresh scratch  | 200, 50 cards     |

- FACT: a fresh Playwright profile under the same automation and the same IP
  gets 200. Therefore neither automation nor IP is blocked.
- FACT (cookie database of the avito profile): Avito challenge cookies are
  short-lived (`_avisc` was sent with `Max-Age=60` in HTTP headers; several
  cookies in this profile are session cookies, expiry 0).
- FACT (Phase 1 test, 2026-11-25, local server): session cookies do not survive
  a Firefox restart in this setup; cookies with an expiry date do.
- FACT (browser history databases): the user's manual Avito visits at 16:40 and
  16:48 local time were recorded in the DEFAULT profile
  (`~/.config/mozilla/firefox/dv1kd7y1.default-esr`), not in
  `~/browser-data/profiles/avito`. The avito profile history shows only script
  runs.
- FACT: after the user completed the challenge in the default-profile Firefox,
  a verification run on the avito profile still returned HTTP 429.

## Inferences

- INFERENCE: QRATOR ties the block to the profile's session state (cookies),
  not to the IP or the automation.
- INFERENCE: the "normal page" the user saw was in the default-profile window;
  the challenge completion never reached the parser's profile. This is why the
  verification run still failed.
- INFERENCE (not yet verified): a challenge completed in the correct profile
  may also be lost if the browser closes before extraction, because the
  clearance likely lives in short-lived cookies.

## Workflow conclusions

1. Recovery must happen in the SAME profile the parser uses, and extraction
   must continue in the SAME browser session (CLAUDE.md 7.1). Do not close the
   browser between the challenge and extraction.
2. The agent must not mask automation or solve the challenge (CLAUDE.md 8.3).
   Human-in-the-loop over VNC is the sanctioned path.
3. When the agent asks the user to act in "the window", it must name the exact
   browser instance (the parser's profile), because a second Firefox is often
   running.

## Recovery procedure (verified 2026-11-27)

When the avito profile is flagged (challenge page on every run) and the user
prefers not to complete the challenge over VNC, reset the session state of the
profile. This needs user approval (persistent profile change).

1. Make sure no Firefox is using the profile (CLAUDE.md 6.2).
2. Delete the Avito cookies from the profile (keep everything else):

       cd ~/browser-data/profiles/avito && ~/.venvs/web-lab-playwright/bin/python -c \
         "import sqlite3; c=sqlite3.connect('cookies.sqlite');
         n=c.execute(\"select count(*) from moz_cookies where host like '%avito%'\").fetchone()[0];
         c.execute(\"delete from moz_cookies where host like '%avito%'\"); c.commit();
         print('deleted', n)"

3. Run the parse again.

FACT: after this reset (40 Avito cookies deleted) the run delivered the real
search page with 50 listings and all schema fields. No challenge needed to be
completed. OBSERVATION: the initial document response status was 439 (the
security-check status) but the page resolved itself in JavaScript and delivered
full content (384 request events). The run validates by content, not by HTTP
status.

## Runbook    ~/.venvs/web-lab-playwright/bin/python parsing/run_avito_search.py

The script opens `~/browser-data/profiles/avito` in headed Firefox on
`DISPLAY=:0`, navigates once to the search URL, and if a challenge page appears
it pauses and waits (up to 10 minutes) for the user to complete the challenge
in THAT window over VNC. Extraction, validation and output happen in the same
session. Output goes to `~/browser-data/data/avito-search.jsonl` (schema
fields only) and the request log to `~/browser-data/logs/`. Test data only;
no real data is kept (user decision, 2026-11-27).

## Status at time of writing

- First human-loop run of `parsing/run_avito_search.py`: see
  DEVELOPMENT_PLAN.md for the verified result.
- UNKNOWN: how long the profile stays clean after a human challenge.
- UNKNOWN: which cookie carries the clearance.
