#!/usr/bin/env python3
"""Alpha check: a Firefox profile cannot be opened by a second session while
the first session holds it, and opens again after release.

Local only: no network requests. Uses a throwaway profile under /tmp/opencode.
Run with the Playwright venv:
    ~/.venvs/web-lab-playwright/bin/python tests/browser/profile_lock_test.py
Exit code 0 = PASS, 1 = FAIL.
"""
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

HOLD_SECONDS = 25
PROFILE_PARENT = Path("/tmp/opencode")


def hold(profile):
    with sync_playwright() as p:
        ctx = p.firefox.launch_persistent_context(profile, headless=True)
        print("holder: opened", flush=True)
        time.sleep(HOLD_SECONDS)
        ctx.close()
        print("holder: closed", flush=True)


def try_open(profile):
    """Return (opened, error_text)."""
    try:
        with sync_playwright() as p:
            ctx = p.firefox.launch_persistent_context(profile, headless=True, timeout=20000)
            ctx.close()
            return True, ""
    except Exception as exc:
        return False, str(exc)


def main():
    PROFILE_PARENT.mkdir(parents=True, exist_ok=True)
    workdir = Path(tempfile.mkdtemp(prefix="lock-test-", dir=PROFILE_PARENT))
    profile = str(workdir / "profile")
    holder = None
    try:
        holder = subprocess.Popen(
            [sys.executable, __file__, "--hold", profile],
            stdout=subprocess.PIPE, text=True,
        )
        if holder.stdout.readline().strip() != "holder: opened":
            print("FAIL: holder could not open the profile")
            return 1

        opened_while_held, err = try_open(profile)
        refused_reason_ok = "already running" in err
        print(f"second session while held: opened={opened_while_held} "
              f"refused_with_lock_message={refused_reason_ok}")

        holder.wait(timeout=HOLD_SECONDS + 30)
        opened_after, err_after = try_open(profile)
        print(f"second session after release: opened={opened_after}")

        passed = (not opened_while_held) and refused_reason_ok and opened_after
        print("RESULT:", "PASS" if passed else "FAIL")
        if not passed and err_after:
            print("last error:", err_after.splitlines()[0])
        return 0 if passed else 1
    finally:
        if holder and holder.poll() is None:
            holder.kill()
        shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--hold":
        hold(sys.argv[2])
    else:
        sys.exit(main())
