#!/usr/bin/env python3
"""Replaces `cat`. Usage: python3 scripts/read_file.py <path>"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script_logger import log_invocation, log_result

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/read_file.py <path>")
        sys.exit(1)
    path = sys.argv[1]
    log_invocation("read_file.py", [path])
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        print(content)
        log_result("read_file.py", "OK", path)
    except Exception as e:
        log_result("read_file.py", "ERROR", str(e))
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
