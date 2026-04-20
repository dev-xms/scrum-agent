import sys
import os
import datetime
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script_logger import log_invocation, log_result

# --- Directory Contract Configuration ---
# Defines which phase is allowed to write to which directories/files
PHASE_PERMISSIONS = {
    "1": {"write": ["logs/log.md"], "read": ["references/", "requirements/"]},
    "2": {"write": ["logs/log.md", "design/", "architecture/"], "read": ["logs/log.md", "src/"]},
}

def enforce_append_only_log(session_id, phase, message):
    log_file = "logs/log.md"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] [{session_id}] [PHASE {phase}] {message}\n"
    try:
        with open(log_file, "a", encoding="utf-8") as f:  # Force 'a' (append) mode to prevent accidental 'w' (overwrite)
            f.write(entry)
        print(f"Success: Logged Phase {phase} activity.")
    except Exception as e:
        print(f"Error: Failed to write to log.md: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Scrum Agent Gatekeeper & Logger")
    parser.add_argument("--phase", required=True, help="Current SDLC Phase (1-6)")
    parser.add_argument("--session", required=True, help="Current Claude Session ID")
    parser.add_argument("--msg", required=True, help="Message to log")
    parser.add_argument("--check_dir", help="Directory the agent is attempting to write to")

    args = parser.parse_args()
    log_invocation("scrum_guard.py", [f"--phase={args.phase}", f"--msg={args.msg}"])

    # 1. Enforce Directory Contract if a check_dir is provided
    if args.check_dir and args.phase in PHASE_PERMISSIONS:
        allowed_dirs = PHASE_PERMISSIONS[args.phase]["write"]
        if not any(args.check_dir.startswith(d) or args.check_dir == d for d in allowed_dirs):
            log_result("scrum_guard.py", "FAILED", f"phase {args.phase} not authorized to write {args.check_dir}")
            print(f"CRITICAL ERROR: Phase {args.phase} is NOT authorized to write to '{args.check_dir}'.")
            sys.exit(1)

    # 2. Perform Append-Only Logging
    enforce_append_only_log(args.session, args.phase, args.msg)
    log_result("scrum_guard.py", "OK", f"phase={args.phase}")

if __name__ == "__main__":
    main()
