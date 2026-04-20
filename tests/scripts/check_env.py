#!/usr/bin/env python3
"""Check required environment dependencies before Phase 3 E2E spec generation."""
import subprocess
import sys


def check(name, cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    ok = result.returncode == 0
    status = "OK" if ok else "MISSING"
    detail = result.stdout.strip() or result.stderr.strip()
    print(f"[{status}] {name}: {detail[:80]}")
    return ok


def main():
    checks = [
        ("node", ["node", "--version"]),
        ("npx", ["npx", "--version"]),
        ("playwright", ["npx", "playwright", "--version"]),
    ]
    results = [check(name, cmd) for name, cmd in checks]
    if all(results):
        print("\nEnvironment ready for E2E specs.")
        sys.exit(0)
    else:
        print("\nEnvironment NOT ready. Install missing deps before Phase 3 E2E.")
        sys.exit(1)


if __name__ == "__main__":
    main()
