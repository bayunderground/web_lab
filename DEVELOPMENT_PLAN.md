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
8. Test data file `~/browser-data/data/avito-dev-sample.jsonl` (50 rows, dev test only). User says no real data is kept. Delete only with user approval.

## Open decisions

- Backups (CLAUDE.md section 6.7): _deferred_. Testing environment, no live data. Decide destination (not the microSD card), schedule and retention once a real login session or valuable data exists.
- Avito research questions and the extraction schema (which fields to store): _undecided_
- Python web framework (FastAPI, Flask or Django): _to be evaluated in Phase 4_
- PostgreSQL: _deferred until the data model is known_

## Decision records and experiment reports

None yet. Link them here when created (docs/decisions/, docs/experiments/).
