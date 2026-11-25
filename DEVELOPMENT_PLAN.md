# DEVELOPMENT_PLAN.md — Web Lab

Current phase, status and open decisions. Rules live in CLAUDE.md; this file holds progress.
Rule: mark a step done only when it has actually been verified, and note how.

## Current status

- **Current phase:** PHASE 0 — Environment audit
- **Last updated:** (fill in on each update)
- **Verified so far:** nothing. No code or commands have been run on Web Lab yet.

## Phase checklist

- [ ] PHASE 0 — Environment audit (Raspberry Pi, Ubuntu PC, VPN, Avito reachability)
- [ ] PHASE 1 — Browser laboratory (Firefox, persistent profiles, Playwright on ARM64, VNC)
- [ ] PHASE 2 — OpenCode integration
- [ ] PHASE 3 — Avito parsing
- [ ] PHASE 4 — Website development
- [ ] PHASE 5 — Optimization
- [ ] PHASE 6 — Controlled autonomy

## Next steps

1. Audit the Raspberry Pi (read-only inspection, report findings).
2. Audit the Ubuntu PC.
3. Check VPN and Avito connectivity from the Pi.

## Open decisions

- Backups (CLAUDE.md section 6.7): _deferred_. Testing environment, no live data. Decide destination (not the microSD card), schedule and retention once a real login session or valuable data exists.
- Avito research questions and the extraction schema (which fields to store): _undecided_
- Python web framework (FastAPI, Flask or Django): _to be evaluated in Phase 4_
- PostgreSQL: _deferred until the data model is known_

## Decision records and experiment reports

None yet. Link them here when created (docs/decisions/, docs/experiments/).
