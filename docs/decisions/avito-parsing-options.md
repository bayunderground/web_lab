# Avito parsing options (research, not yet tested)

Date: 2026-11-25
Status: Proposed. Nothing below is installed or tested on the Pi.
Labels: FACT = read in documentation or observed on the Pi. ASSUMPTION = not tested. UNKNOWN = not determined.

## Context

- Avito returned HTTP 403 (VPN on) and HTTP 429 from QRATOR (VPN off) to plain HTTP HEAD requests from the Pi. See `docs/experiments/phase0-pi-audit.md`.
- FACT: Avito's servers sit behind QRATOR (bot and rate protection).
- FACT: the Pi is aarch64, Debian 13. Firefox, Playwright, and Docker are not installed.
- Rules that apply: CLAUDE.md sections 7 and 8.3. No CAPTCHA solving, no access-control bypass, no ignoring rate limits. Human-assisted login through VNC is allowed.

## Options

### 1. Stock Firefox + Playwright (Python)

- FACT: Playwright drives Firefox through its own Juggler protocol (from Camoufox's documentation). Stock Playwright Firefox support is not verified here.
- ASSUMPTION: a stock Firefox profile may still be flagged by QRATOR.
- ASSUMPTION: needs `apt install firefox-esr` (approval required) and `pip install playwright` in a venv (approval required). ARM64 support: UNKNOWN until installed.
- Fit with CLAUDE.md: matches the initial browser choice (Firefox), keeps the dependency list small.

### 2. Camoufox (patched Firefox + Playwright launcher)

- FACT (camoufox README, GitHub): a Firefox fork for scraping. Driven by Playwright. Per-launch fingerprint identity. Uses a persistent-profile-friendly API (`Camoufox(...)`), and `NewContext()` for per-context identities.
- FACT: install is `pip install -U "camoufox[geoip]"` then `camoufox fetch`, which downloads a prebuilt browser binary.
- FACT: the README says the project is "under development" and "may not be suitable for stable production use".
- FACT: Camoufox is a Firefox build, so it matches CLAUDE.md's preference for Firefox and avoids a second engine.
- UNKNOWN: whether `camoufox fetch` publishes an ARM64 Linux build. The README did not confirm this. Must be checked before any install.
- UNKNOWN: how often Camoufox binaries are updated, and whether they carry the same persistent-profile behaviour as stock Firefox.
- Concern: a third-party binary running with a persistent authenticated profile. The profile would sit in a third-party build. This needs a decision.

### 3. curl_cffi (HTTP client with browser TLS/HTTP2 fingerprints, no JavaScript)

- FACT (GitHub README): Python binding for curl-impersonate. Impersonates Chrome, Firefox, Safari TLS/JA3 and HTTP/2 fingerprints. No JavaScript execution.
- FACT: pure HTTP. Fits CLAUDE.md 7 ("check whether plain HTTP is enough first").
- ASSUMPTION: QRATOR may still block it, because the challenge may need JavaScript. Not tested.
- UNKNOWN: whether it has ARM64 wheels for Python 3.13. Must be checked.
- Fit: cheapest test. Could tell whether a browser is needed at all, and it avoids the rate-limit issue that a browser would add.

### 4. Official Avito API

- OBSERVATION: `api.avito.ru` resolves to 176.114.120.52 (and the other Avito /24s). The domain exists.
- UNKNOWN: whether the API is open to this project, its terms, quotas, and data scope. Not checked. Must be checked against Avito's developer documentation before use.
- CLAUDE.md 8.3 prefers official APIs when they exist. This option should be checked first, before any scraping.

### 5. Persistent browser with human-assisted login (VNC)

- FACT: required by CLAUDE.md section 7 for login and CAPTCHA.
- Applies to all browser options (1, 2). Not an alternative to them.

## Comparison (research only)

| Option | Browser? | Needs approval to test | Main unknown |
|---|---|---|---|
| 0. Avito official API | No | No (documentation read) | Access terms and scope |
| 3. curl_cffi | No | pip install | ARM64 wheel, QRATOR behaviour |
| 1. Stock Firefox + Playwright | Yes | apt + pip | ARM64, QRATOR behaviour |
| 2. Camoufox | Yes | pip + binary download | ARM64 build, trust in third-party binary |

## Recommended test order (after approval)

1. Read Avito's official API documentation (no requests to Avito). Decide whether it covers the data needed.
2. If no API covers it: test curl_cffi with a single GET, respecting rate limits. Stop on any 403 or 429.
3. If HTTP is blocked: test stock Firefox + Playwright on the Pi, one profile, one page, with a human-visible VNC session.
4. Camoufox only if stock Firefox is blocked and a decision is made to accept a third-party browser build.

## Open questions for the user

- Do you want to read Avito's official API docs first (step 1)?
- Is Camoufox acceptable given the third-party binary, or should we stay with stock Firefox?
- Research queries for QRATOR behaviour failed (web search unavailable). Only GitHub README pages were read.

## Network exceptions (done this session)

- `~/domains-to-cidr/networks.txt`: appended `46.42.187.0/24` (static.avito.ru) and `151.236.103.0/24` (www.avito.st). Backup copy: `~/domains-to-cidr/networks.txt.bak-2026-11-25` (untracked, not in git). Also in `/tmp/opencode/`.
- Other Avito hosts (`api.avito.ru`, `gw.avito.ru`, `avito.st`, `m.avito.ru`, `*.img.avito.st`) resolve to /24s already listed.
- `failed-domains.txt` entries are `www.`-prefixed. The real hosts (for example `00.img.avito.st`) resolve. Not edited.
