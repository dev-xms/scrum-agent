#!/usr/bin/env python3
"""Run Playwright E2E tests for a given BKI. Starts HTTP server, runs tests, stops server."""
import subprocess
import sys
import time
import signal
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: run_e2e_tests.py <BKI-ID|regression> [sprint-folder]")
        sys.exit(1)

    bki = sys.argv[1].upper()
    sprint_folder = sys.argv[2] if len(sys.argv) >= 3 else None

    if bki == "REGRESSION":
        spec_path = "tests/e2e/"
        artifact_name = "regression_e2e.txt"
    else:
        spec_path = f"tests/e2e/{bki}.spec.js"
        artifact_name = f"{bki}_e2e.txt"

    base_dir = f"tests/results/{sprint_folder}" if sprint_folder else "tests/results"
    pw_output_dir = f"{base_dir}/playwright"
    cmd = ["npx", "playwright", "test", spec_path, "--config", "playwright.config.js",
           "--reporter=line", "--output", pw_output_dir]

    server = subprocess.Popen(
        ["python3", "-m", "http.server", "8080", "--directory", "src"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    time.sleep(1)

    try:
        if sprint_folder:
            artifact_dir = Path(f"tests/results/{sprint_folder}")
            artifact_dir.mkdir(parents=True, exist_ok=True)
            artifact_path = artifact_dir / artifact_name
            result = subprocess.run(cmd, capture_output=True, text=True)
            artifact_path.write_text(result.stdout + result.stderr)
            print(result.stdout)
            if result.stderr:
                print(result.stderr)
            returncode = result.returncode
        else:
            result = subprocess.run(cmd, capture_output=False)
            returncode = result.returncode
    finally:
        server.send_signal(signal.SIGTERM)
        server.wait()

    sys.exit(returncode)


if __name__ == "__main__":
    main()
