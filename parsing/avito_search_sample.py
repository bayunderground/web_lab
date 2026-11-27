#!/usr/bin/env python3
"""Alpha: parse one Avito search results page and validate the output.

One navigation, saved persistent profile, no HTML saved. Output is JSONL with
the fields below, written under ~/browser-data/data (outside Git).
Needs a display for headed Firefox (on the Pi: DISPLAY=:0).

    DISPLAY=:0 XAUTHORITY=$HOME/.Xauthority \
      ~/.venvs/web-lab-playwright/bin/python parsing/avito_search_sample.py
Exit code 0 = PASS (validation passed), 1 = FAIL.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

PROFILE = str(Path.home() / "browser-data/profiles/avito")
SEARCH_URL = "https://www.avito.ru/all/avtomobili?cd=1"
OUT_FILE = Path.home() / "browser-data/data/avito-search-sample.jsonl"
REQUEST_LOG = Path.home() / "browser-data/logs/avito-search-requests.jsonl"
MAX_CARDS = 50

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


def fetch(request_log):
    with sync_playwright() as p:
        ctx = p.firefox.launch_persistent_context(PROFILE, headless=False)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        def on_request(req):
            request_log.append({
                "time": datetime.now(timezone.utc).isoformat(),
                "event": "request",
                "method": req.method,
                "url": req.url,
                "resource_type": req.resource_type,
            })

        def on_response(resp):
            request_log.append({
                "time": datetime.now(timezone.utc).isoformat(),
                "event": "response",
                "status": resp.status,
                "url": resp.url,
            })

        page.on("request", on_request)
        page.on("response", on_response)
        response = page.goto(SEARCH_URL, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(3000)
        html = page.content()
        result = {
            "http_status": response.status if response else None,
            "final_url": page.url,
            "blocked": any(m in html for m in ["Доступ ограничен", "проверка безопасности"]),
            "rows": page.evaluate(ITEMS_JS, MAX_CARDS),
        }
        ctx.close()
        return result


def validate(result, fetched_at):
    rows = []
    for item in result["rows"]:
        rows.append({
            "source_url": SEARCH_URL,
            "final_url": result["final_url"],
            "fetched_at": fetched_at,
            "http_status": result["http_status"],
            **item,
        })
    checks = {
        "http_200": result["http_status"] == 200,
        "not_blocked": not result["blocked"],
        "cards_found": len(rows) > 0,
        "titles_present": all(r["title"] for r in rows),
        "prices_present": all(r["price"] for r in rows),
        "hrefs_present": all(r["href"] for r in rows),
        "hrefs_unique": len({r["href"] for r in rows}) == len(rows),
    }
    return rows, checks


def main():
    fetched_at = datetime.now(timezone.utc).isoformat()
    request_log = []
    result = fetch(request_log)
    rows, checks = validate(result, fetched_at)

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUT_FILE.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    REQUEST_LOG.parent.mkdir(parents=True, exist_ok=True)
    with REQUEST_LOG.open("w", encoding="utf-8") as f:
        for entry in request_log:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print("request log:", len(request_log), "events ->", REQUEST_LOG)

    print("status:", result["http_status"], "| final_url:", result["final_url"])
    print("rows:", len(rows), "->", OUT_FILE)
    for name, ok in checks.items():
        print(f"  {name}: {'ok' if ok else 'FAIL'}")
    passed = all(checks.values())
    print("RESULT:", "PASS" if passed else "FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
