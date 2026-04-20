#!/usr/bin/env python3
"""
Gate script: create a directory (and parents) if it doesn't exist.
Usage: python3 scripts/make_dir.py <path>
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script_logger import log_invocation, log_result

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/make_dir.py <path>")
        sys.exit(1)

    path = sys.argv[1]
    log_invocation("make_dir.py", [path])

    os.makedirs(path, exist_ok=True)
    log_result("make_dir.py", "OK", path)
    print(f"OK: {path}")

if __name__ == "__main__":
    main()
