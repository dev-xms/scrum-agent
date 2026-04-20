#!/usr/bin/env python3
"""Check if @playwright/test package is resolvable in the project (local or global)."""
import subprocess
import sys


def main():
    checks = [
        ("@playwright/test (local node_modules)", ["node", "-e", "require('@playwright/test'); console.log('ok')"]),
        ("playwright global version", ["npx", "playwright", "--version"]),
    ]
    all_ok = True
    for name, cmd in checks:
        result = subprocess.run(cmd, capture_output=True, text=True)
        ok = result.returncode == 0 and "ok" in result.stdout or result.returncode == 0
        status = "OK" if result.returncode == 0 else "MISSING"
        detail = (result.stdout.strip() or result.stderr.strip())[:100]
        print(f"[{status}] {name}: {detail}")
        if result.returncode != 0:
            all_ok = False

    if not all_ok:
        print("\nFix: run `npm init -y && npm install @playwright/test && npx playwright install`")
        sys.exit(1)
    print("\nPlaywright test package ready.")


if __name__ == "__main__":
    main()
