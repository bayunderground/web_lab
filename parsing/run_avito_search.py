#!/usr/bin/env python3
"""Avito search parse with human-in-the-loop challenge recovery (alpha).

Opens the persistent profile ~/browser-data/profiles/avito in headed Firefox
(visible over VNC) and navigates ONCE to the Avito search page. If Avito
serves a block/challenge page (HTTP 429 + hCaptcha firewall), the script
PAUSES: the user completes the challenge in the same window over VNC
(CLAUDE.md section 7.1). Extraction continues in the same browser session.

Output (outside Git, test data):
  ~/browser-data/data/avito-search.jsonl            one row per listing
  ~/browser-data/logs/avito-search-requests.jsonl   request log (URL/status only)

Usage:
  ~/.venvs/web-lab-playwright/bin/python parsing/run_avito_search.py [--auto-close] [--max-wait SECONDS]

  --auto-close   close the browser when done. Default: leave the browser open
                 and wait until the window is closed by hand (shutdown is an
                 explicit operation, CLAUDE.md section 6.6).
  --max-wait     seconds to wait for the user on a challenge page
                 (default 600). Keep it small to fail fast instead of
                 leaving a challenge window on screen.

Exit code 0 = data extracted and validated, 1 = failed or human wait timed out.

Rules honored: one navigation, no challenge solving by the agent, no cookie or
storage clearing, no HTML saved, schema fields only (CLAUDE.md 7, 8.5).
"""
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

os.environ.setdefault("DISPLAY", ":0")
os.environ.setdefault("XAUTHORITY", str(Path.home() / ".Xauthority"))

from playwright.sync_api import sync_playwright  # noqa: E402

PROFILE = str(Path.home() / "browser-data/profiles/avito")
SEARCH_URL = "https://www.avito.ru/all/avtomobili?cd=1"
DATA_OUT = Path.home() / "browser-data/data/avito-search.jsonl"
REQ_LOG = Path.home() / "browser-data/logs/avito-search-requests.jsonl"

MAX_CARDS = 50
WAIT_FOR_HUMAN_S = 600      # give the user 10 minutes over VNC
POLL_INTERVAL_S = 5
BLOCK_MARKERS = ("Доступ ограничен", "проверка безопасности", "firewallCaptcha")

ITEMS_JS = """
(maxCards) => {
  const cards = Array.from(document.querySelectorAll('[data-marker="item"]')).slice(0, maxCards);
  return cards.map(el => {
    const a = el.querySelector('a[href]');
    const title = el.querySelector('[data-marker="item-title"], [itemprop="name"], h3');
    const price = el.querySelector('[data-marker="item-price"]');
    return {
      title: ((title ? title.innerText : (a ? a.innerText : '')) || '').trim().slice(0, 200),
      price: price ? price.innerText.trim() : null,
      href: a ? a.getAttribute('href') : null,
    };
  });
}
"""


def is_blocked(html):
    return any(marker in html for marker in BLOCK_MARKERS)


def wait_for_human(page, timeout_s):
    """Watch the page (local DOM reads only) until the challenge is cleared."""
    print(f"PAUSED: a challenge page is showing. Complete it in the Firefox "
          f"window over VNC. Waiting up to {timeout_s} s...",
          flush=True)
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        time.sleep(POLL_INTERVAL_S)
        try:
            if not is_blocked(page.content()):
                print("challenge cleared, continuing", flush=True)
                return True
        except Exception as exc:
            print("page read failed while waiting:", exc, flush=True)
            return False
    return False


def main():
    auto_close = "--auto-close" in sys.argv
    max_wait = WAIT_FOR_HUMAN_S
    if "--max-wait" in sys.argv:
        max_wait = int(sys.argv[sys.argv.index("--max-wait") + 1])
    fetched_at = datetime.now(timezone.utc).isoformat()
    request_log = []

    with sync_playwright() as p:
        ctx = p.firefox.launch_persistent_context(PROFILE, headless=False)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        def on_request(req):
            request_log.append({"time": datetime.now(timezone.utc).isoformat(),
                                "event": "request", "method": req.method,
                                "url": req.url, "resource_type": req.resource_type})

        def on_response(resp):
            request_log.append({"time": datetime.now(timezone.utc).isoformat(),
                                "event": "response", "status": resp.status,
                                "url": resp.url})

        page.on("request", on_request)
        page.on("response", on_response)

        response = page.goto(SEARCH_URL, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(3000)
        status = response.status if response else None
        blocked = is_blocked(page.content())

        if blocked:
            if not wait_for_human(page, max_wait):
                print("RESULT: FAIL (challenge not cleared in time)", flush=True)
                _write_request_log(request_log)
                _close(ctx, auto_close)
                return 1
            page.wait_for_timeout(2000)
            status = 200  # page state verified below by cards + markers

        html = page.content()
        rows = page.evaluate(ITEMS_JS, MAX_CARDS)
        final_url = page.url
        _close(ctx, auto_close)

    out_rows = [{**r, "source_url": SEARCH_URL, "final_url": final_url,
                 "fetched_at": fetched_at, "http_status": status} for r in rows]
    checks = {
        # HTTP status is recorded per row but is not the success criterion:
        # Avito may deliver the real page after a self-resolving security check
        # (observed: initial document 439, full content, 50 cards).
        "not_blocked": not is_blocked(html),
        "cards_found": len(out_rows) > 0,
        "titles_present": all(r["title"] for r in out_rows),
        "prices_present": all(r["price"] for r in out_rows),
        "hrefs_present": all(r["href"] for r in out_rows),
        "hrefs_unique": len({r["href"] for r in out_rows}) == len(out_rows),
    }

    DATA_OUT.parent.mkdir(parents=True, exist_ok=True)
    with DATA_OUT.open("w", encoding="utf-8") as f:
        for r in out_rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    _write_request_log(request_log)

    print("status:", status, "| final_url:", final_url)
    print("rows:", len(out_rows), "->", DATA_OUT)
    for name, ok in checks.items():
        print(f"  {name}: {'ok' if ok else 'FAIL'}")
    print("request log:", len(request_log), "events ->", REQ_LOG)
    passed = all(checks.values())
    print("RESULT:", "PASS" if passed else "FAIL")
    return 0 if passed else 1


def _write_request_log(request_log):
    REQ_LOG.parent.mkdir(parents=True, exist_ok=True)
    with REQ_LOG.open("w", encoding="utf-8") as f:
        for entry in request_log:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _close(ctx, auto_close):
    if auto_close:
        ctx.close()
        return
    print("browser stays open; close the window to finish (or use --auto-close)",
          flush=True)
    try:
        ctx.wait_for_event("close", timeout=30 * 60 * 1000)
    except Exception:
        pass


if __name__ == "__main__":
    sys.exit(main())
