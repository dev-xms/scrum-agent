#!/usr/bin/env python3
"""Replaces `ls`. Usage: python3 scripts/list_dir.py [path]"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script_logger import log_invocation, log_result

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    log_invocation("list_dir.py", [path])
    try:
        entries = sorted(os.listdir(path))
        for e in entries:
            print(e)
        log_result("list_dir.py", "OK", path)
    except Exception as e:
        log_result("list_dir.py", "ERROR", str(e))
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
