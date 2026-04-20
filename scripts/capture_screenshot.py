#!/usr/bin/env python3
"""
Gate script: start static server, capture Playwright screenshot, kill server.
Usage: python3 scripts/capture_screenshot.py BKI-XXX [sprint-folder]
sprint-folder defaults to BKI-XXX if omitted.
"""
import sys, os, subprocess, time, signal
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script_logger import log_invocation, log_result

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/capture_screenshot.py <BKI-ID> [sprint-folder]")
        sys.exit(1)

    bki = sys.argv[1]
    sprint_folder = sys.argv[2] if len(sys.argv) >= 3 else bki
    log_invocation("capture_screenshot.py", [bki, sprint_folder])
    artifact_dir = f"test-results/{sprint_folder}"
    os.makedirs(artifact_dir, exist_ok=True)
    output = f"{artifact_dir}/{bki}_ui.png"

    server = subprocess.Popen(
        ["npx", "serve", "src", "-p", "3000", "-s"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    time.sleep(2)

    try:
        result = subprocess.run(
            ["npx", "playwright", "screenshot", "--browser", "chromium",
             "http://localhost:3000", output],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            log_result("capture_screenshot.py", "FAILED", result.stderr.strip())
            print(f"GATE FAILED: Screenshot capture failed.\n{result.stderr}")
            sys.exit(1)
        log_result("capture_screenshot.py", "OK", output)
        print(f"GATE PASSED: Screenshot saved to {output}")
    finally:
        server.send_signal(signal.SIGTERM)
        server.wait()

if __name__ == "__main__":
    main()
