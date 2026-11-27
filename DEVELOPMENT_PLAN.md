# DEVELOPMENT_PLAN.md — Web Lab

Current phase, status and open decisions. Rules live in CLAUDE.md; this file holds progress.
Rule: mark a step done only when it has actually been verified, and note how.

## Current status

- **Current phase:** PHASE 0 — Environment audit
- **Last updated:** 2026-11-25
- **Verified so far:**
  - Pi read-only audit: OS, kernel, CPU, RAM, storage, installed software, network routes, DNS, listening services. Report: `docs/experiments/phase0-pi-audit.md`.
  - Avito: one HEAD request from the Pi returned HTTP 403 (VPN on). After the VPN was disabled, a second HEAD request returned HTTP 429 (QRATOR). Not retried further (AGENTS.md section 7). Cause not established.
  - Git remote `origin` points to `https://github.com/bayunderground/web_lab.git`.
  - Installed on Pi (2026-11-25, with sudo approval): `firefox-esr` 153.7.0esr (apt), Playwright 1.65.2 in `~/.venvs/web-lab-playwright` (outside repo).
  - Smoke test (`/tmp/opencode/ff_smoke.py`): Playwright headless Firefox 159.0 launched, rendered a local page and read its DOM in 3.0 s. Verified on local content only. `navigator.webdriver` = true (automation signal, not yet addressed).
  - curl_cffi 0.17.0 installed in the same venv. Smoke test: `impersonate="chrome"` GET to a local server on 127.0.0.1 returned 200. Verified locally only.
  - Not done on purpose: no Avito requests (429 rate limit), no `navigator.webdriver` masking (would evade bot detection, CLAUDE.md 8.3).
  - Avito via curl_cffi (`impersonate="chrome"`, VPN on, 2026-11-25): first GET returned HTTP 200 from QRATOR with a 1.18 MB body and no `<title>`. Not parsed further. A second GET, made by mistake while inspecting that body, returned HTTP 439 with the title "Доступ ограничен: проверка безопасности" (access restricted, security check). Treat as access denied. No more requests. Body not saved.
  - Decision (user, 2026-11-25): do not use the Avito official API. No cooldown wait required by user. Agent still will not retry a denied (439) request: CLAUDE.md 7 requires stopping. Path forward that fits the rules: human completes the security check via VNC in a persistent Firefox profile, then the agent resumes (CLAUDE.md 7.1). Needs user approval to create the profile.
  - Persistent Avito profile created: `~/browser-data/profiles/avito` (mode 700, outside repo). Headed Firefox ESR (PID 19939, `-no-remote`) started on Wayland display `wayland-0` (labwc session), opened to `about:blank`. Not yet visually verified on VNC. Log: `~/browser-data/firefox-avito.log`. Separate from the user's default Firefox (PID 17414, default profile), which was left running.
  - Avito via Firefox (2026-11-25, after user confirmed normal Avito layout in the VNC Firefox):
    - Closed the VNC Firefox (PID 19939) with SIGTERM. Clean exit confirmed. `.parentlock` file still present; Playwright launched fine.
    - Option 1 first attempt failed at launch: no `DISPLAY` set. Not a request. Cause: Playwright's Firefox needs X11, and the labwc session has XWayland on `:0`.
    - Option 1 retry with `DISPLAY=:0`, headed, persistent profile `~/browser-data/profiles/avito`: ONE navigation to `https://www.avito.ru/`. Result: HTTP 200, final URL `https://www.avito.ru/`, title "Авито — Объявления на сайте Авито". No block markers ("Доступ ограничен", "проверка безопасности", QRATOR: 0). One "captcha" string in the HTML, not investigated.
    - Verified: the page loads normally through Playwright with the saved profile. Not verified: listing extraction, pagination, session reuse across restarts.
    - Extraction attempt (dev sample, 2026-11-25): ONE more navigation to `https://www.avito.ru/` with the saved profile. HTTP 200, 466 `data-marker` elements, 111 internal links. Item-card selector `[data-marker^="item"]` matched 0 cards, so 0 rows written. Output file `~/browser-data/data/avito-dev-sample.jsonl` is empty. Selectors need markup inspection. Not verified: any listing data.
    - Cause of 0 items: homepage cards use `data-marker="bx-recommendations-block-item"` (37 prices on homepage), which `^="item"` does not match.
    - Two-page run (2026-11-25, same profile, two navigations, no HTML saved):
      - Homepage `https://www.avito.ru/`: HTTP 200, markers confirmed (item-price, item-photo, item-location).
      - Search `https://www.avito.ru/all/avtomobili?cd=1`: HTTP 200, final URL unchanged. 50 item cards (`data-marker="item"`). Output `~/browser-data/data/avito-dev-sample.jsonl`: 50 rows, 50 non-empty titles, 50 unique hrefs, 50 with price.
      - Data quality notes (not validated against a schema): the price field can include credit text ("от 35 723 ₽ в месяц"). Hrefs carry a `?context=` tracking parameter. Location prompt still appears, and the profile has no stored geolocation permission record.
    - Deviation from CLAUDE.md 6.6: the script closed the browser on exit. Browser is no longer running. Profile preserved. Stopped because access is now restricted (CLAUDE.md 7, 8.3).
  - Session reuse check (2026-11-25, user approved a few requests): ONE navigation to `https://www.avito.ru/all/avtomobili?cd=1` in a new Playwright session on the saved profile, after the earlier browser was closed. HTTP 200, 50 item cards, no block markers. Verified: session reuse across a browser restart. Nothing saved.
  - Git push to `origin` (GitHub) FAILED: "Permission to bayunderground/web_lab.git denied" (HTTP 403). Local commit `845974a` is not pushed. Needs credentials with write access. Not changed by the agent.
  - Dell (`bliss@dell`, read-only inspection, 2026-11-25): Ubuntu 24.04.4, x86_64. `/var/www/mini/web_lab` is at commit `1014afb initial`, clean. Nothing changed there.
  - Push retry with the GitHub token the user provided in chat (2026-11-25): still HTTP 403 "Permission ... denied to bayunderground". Token was used only via a temporary askpass script (deleted), not stored in any file. Recommend the user revokes it and issues a new one with write access to `bayunderground/web_lab`. Still not pushed.
  - Test data file `~/browser-data/data/avito-dev-sample.jsonl` deleted (user approved; test data only).
  - Phase 1 persistent-profile test, local only (no Avito): localStorage written in one browser session was read back after restart (`persisted-42`). Cookie with an expiry date survived the restart. Session cookie (no expiry) did NOT survive. Relevant for Avito, whose session cookies may be session-only.
  - Git push to `origin/main` succeeded after the user fixed the git access problem (2026-11-25). `origin/main` = `b566cdd`.
  - Phase 1, profile locking (local only, 2026-11-25): a second Playwright session on a profile already open in another session was refused by Firefox: "Firefox is already running, but is not responding ... use a different profile". Verified: one profile, one process.
  - Alpha script `tests/browser/profile_lock_test.py` (2026-11-27): rerun of the profile-locking test. PASS: second session refused while held ("already running"), opened after release. Local only. Status: alpha, not reviewed.
  - Avito search parse attempt (2026-11-27), script `parsing/avito_search_sample.py` (alpha, not validated): ONE navigation to `https://www.avito.ru/all/avtomobili?cd=1` with the saved profile. Result: HTTP 429 (rate limit). Validation FAILED (http_200, not_blocked, cards_found). 0 rows written, empty output file removed. No retry. Do not send Avito requests until the rate limit clears and the user approves.
  - Retry after the user added networks to the VPN exceptions (2026-11-27): ONE run of `parsing/avito_search_sample.py`. Still HTTP 429, validation FAILED, 0 rows, output removed. The VPN exception list did not clear the rate limit. No retry. A further run (user-approved, 2026-11-27) also returned 429: FAIL, 0 rows, output removed. Avito requests stopped until the user decides.
  - Run with request logging (2026-11-27, user-approved, one run): HTTP 429 on the search page. Page then loaded an hCaptcha firewall challenge: `POST https://www.avito.ru/web/5/firewallCaptcha/get`, scripts from `hcaptcha.com` and `www.avito.st/s/captcha/gt4.js`. 11 requests in total. Per CLAUDE.md 7: interactive challenge, stop, do not solve, wait for the user over VNC. Request log: `~/browser-data/logs/avito-search-requests.jsonl` (URLs and statuses only, no cookies, headers or bodies). Keep for later analysis. Later runs at the user's request (2026-11-27) also returned 429: same result each time, output removed. The block is stable across the VPN-exception change.
  - Root-cause investigation (2026-11-27, after user reported the page loads in their own Firefox): three-way comparison — system Firefox ESR + default profile (manual): works; Playwright + avito profile: 429 + hCaptcha; Playwright + fresh scratch profile: 200 with 50 cards. FACT: the block is tied to the avito profile's session state, not the IP or automation. Report: `docs/experiments/avito-access-recovery-2026-11-27.md`.
  - The user's challenge completion went to the DEFAULT profile Firefox (history: avito visits 16:40 and 16:48 in `~/.config/mozilla/firefox/dv1kd7y1.default-esr`), not to the avito-profile window. Verification run on the avito profile afterwards: still HTTP 429, FAIL, 0 rows. Lesson recorded in AGENTS.md section 11: when asking the user to act, name the exact window.
  - Runner script saved: `parsing/run_avito_search.py` (human-in-the-loop: one navigation, pause on challenge, extract in the same session, request log kept). Its first human-loop run (2026-11-27): FAIL. The script paused on the challenge page as designed (429 + hCaptcha, request log shows the widget loading at 17:03:51 local), but the browser window was closed while paused, so the page target disappeared before extraction. Next attempt requires the window to stay open while the user completes the challenge.
  - Session-state reset (user approved "clear and run", 2026-11-27): deleted the 40 Avito cookies from the avito profile (nothing else touched). Follow-up run of `parsing/run_avito_search.py`: real search page, 50 rows extracted with all schema fields (title, price, href, unique hrefs), no challenge page to complete. OBSERVATION: initial document status was 439 but the page self-resolved in JavaScript to full content; validation now uses content checks, not HTTP status. Verified: Avito parsing works again from the persistent profile without human challenge. Output kept: `~/browser-data/data/avito-search.jsonl` (test data). UNKNOWN: whether the flag returns and how soon.
  - Not verified: VNC interaction (needs the user to check the screen), recovery after an OpenCode restart, Dell/Ubuntu parity.
  - Not verified: any Avito content parsed successfully. Avito returned 429 again on a GET via VPN (2026-11-25). No further requests until the user decides.
- **Not verified / not done:** Docker is not installed on the Pi. No Ubuntu PC audit. Playwright headed launch needs `DISPLAY=:0` (XWayland). No VNC-session test beyond the Avito profile window.

## Phase checklist

- [ ] PHASE 0 — Environment audit (Raspberry Pi, Ubuntu PC, VPN, Avito reachability)
  - [x] Raspberry Pi read-only audit (done 2026-11-25)
  - [ ] Ubuntu PC audit
  - [ ] Avito reachability: 403 observed; cause unknown; needs user decision
- [ ] PHASE 1 — Browser laboratory (Firefox, persistent profiles, Playwright on ARM64, VNC)
- [ ] PHASE 2 — OpenCode integration
- [ ] PHASE 3 — Avito parsing
- [ ] PHASE 4 — Website development
- [ ] PHASE 5 — Optimization
- [ ] PHASE 6 — Controlled autonomy

## Next steps

1. ~~Audit the Raspberry Pi (read-only inspection, report findings).~~ Done, see `docs/experiments/phase0-pi-audit.md`.
2. Audit the Ubuntu PC.
3. Check VPN and Avito connectivity from the Pi. Partly done: VPN routes inspected; Avito returned 403 (VPN on) and 429 (VPN off). Next step needs the user's decision.
   - Planned design (from user): VPN stays on for LIVE, with exception networks for Avito and related hosts. Networks come from `~/domains-to-cidr`, and the user adds them manually to the exceptions.
   - Open: `failed-domains.txt` lists Avito CDN hosts (`*.img.avito.st`) that have no networks yet. Needs resolution before the exception list is complete.
   - Open: `networks.txt` has /24 entries, while the tool docs say /20. Needs a check.
4. Research Avito parsing options: `docs/decisions/avito-parsing-options.md` (proposed, nothing tested). Decide test order with the user.
5. Exception networks for Avito: `networks.txt` (in `~/domains-to-cidr`) now also has `46.42.187.0/24` and `151.236.103.0/24`. Backup in `~/domains-to-cidr/networks.txt.bak-2026-11-25`. Manual step, done 2026-11-25.
6. ~~Create `.gitignore` before the first commit.~~ Done 2026-11-25 (runtime data, secrets, caches). Checked with `git status` below.
7. ~~Correct CLAUDE.md section 4.1: Pi OS is Debian 13 (trixie), not Bookworm.~~ Done 2026-11-25 (line 321).
8. Test data file `~/browser-data/data/avito-dev-sample.jsonl` (50 rows, dev test only). User says no real data is kept. Delete only with user approval. (Deleted 2026-11-27 earlier; new test output is written again by the runner.)
9. ~~Run `parsing/run_avito_search.py` with the user completing the challenge in the window it opens.~~ Done 2026-11-27 via the session-state reset (no challenge needed): 50 rows extracted and validated.

## Open decisions

- Backups (CLAUDE.md section 6.7): _deferred_. Testing environment, no live data. Decide destination (not the microSD card), schedule and retention once a real login session or valuable data exists.
- Avito research questions and the extraction schema (which fields to store): _undecided_
- Python web framework (FastAPI, Flask or Django): _to be evaluated in Phase 4_
- PostgreSQL: _deferred until the data model is known_

## Decision records and experiment reports

None yet. Link them here when created (docs/decisions/, docs/experiments/).
