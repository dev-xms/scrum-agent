#!/usr/bin/env python3
"""Replaces `cp`. Usage: python3 scripts/copy_file.py <src> <dst>"""
import sys, os, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script_logger import log_invocation, log_result

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 scripts/copy_file.py <src> <dst>")
        sys.exit(1)
    src, dst = sys.argv[1], sys.argv[2]
    log_invocation("copy_file.py", [src, dst])
    try:
        dst_dir = os.path.dirname(dst)
        if dst_dir:
            os.makedirs(dst_dir, exist_ok=True)
        shutil.copy2(src, dst)
        log_result("copy_file.py", "OK", f"{src} -> {dst}")
        print(f"Copied: {src} -> {dst}")
    except Exception as e:
        log_result("copy_file.py", "ERROR", str(e))
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
