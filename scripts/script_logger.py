#!/usr/bin/env python3
"""Shared audit logger. All scripts call log_invocation() on entry and log_result() on exit."""
import datetime, os

LOG_FILE = "logs/scripts-records.log"

def _append(entry: str):
    os.makedirs("logs", exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry + "\n")

def log_invocation(script: str, args: list):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _append(f"[{ts}] [INVOKE] {script} args={args}")

def log_result(script: str, status: str, detail: str = ""):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _append(f"[{ts}] [RESULT] {script} status={status}" + (f" detail={detail}" if detail else ""))
