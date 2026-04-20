#!/usr/bin/env python3
"""Initialize npm + install @playwright/test + install browsers. Run once per project."""
import subprocess
import sys


def run(label, cmd):
    print(f"\n>>> {label}")
    result = subprocess.run(cmd, capture_output=False)
    if result.returncode != 0:
        print(f"FAILED: {label}")
        sys.exit(result.returncode)


def main():
    run("npm init (skip prompts)", ["npm", "init", "-y"])
    run("npm install @playwright/test", ["npm", "install", "@playwright/test"])
    run("playwright install browsers", ["npx", "playwright", "install"])
    print("\nDone. @playwright/test ready.")


if __name__ == "__main__":
    main()
