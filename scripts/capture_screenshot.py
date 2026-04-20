#!/usr/bin/env python3
"""
Gate script: start static server, capture Playwright screenshot, kill server.
Usage: python3 scripts/capture_screenshot.py BKI-XXX
"""
import sys, os, subprocess, time, signal
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script_logger import log_invocation, log_result

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/capture_screenshot.py <BKI-ID>")
        sys.exit(1)

    bki = sys.argv[1]
    log_invocation("capture_screenshot.py", [bki])
    os.makedirs("logs/screenshots", exist_ok=True)
    output = f"logs/screenshots/{bki}_ui.png"

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
