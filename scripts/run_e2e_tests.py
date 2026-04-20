#!/usr/bin/env python3
"""
Gate script: run Playwright E2E tests and save artifact.
Usage: python3 scripts/run_e2e_tests.py BKI-XXX
"""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script_logger import log_invocation, log_result

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/run_e2e_tests.py <BKI-ID>")
        sys.exit(1)

    bki = sys.argv[1]
    log_invocation("run_e2e_tests.py", [bki])
    os.makedirs("logs/test-results", exist_ok=True)
    artifact = f"logs/test-results/{bki}_e2e.txt"

    result = subprocess.run(
        ["npm", "run", "test:e2e"],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )

    with open(artifact, "w") as out:
        out.write(result.stdout)

    print(result.stdout)
    print(f"\nArtifact saved: {artifact}")

    if result.returncode != 0:
        log_result("run_e2e_tests.py", "FAILED", f"E2E failed for {bki}")
        print(f"GATE FAILED: E2E tests did not pass for {bki}.")
        sys.exit(1)

    log_result("run_e2e_tests.py", "OK", f"E2E green for {bki}")
    print(f"GATE PASSED: E2E tests green for {bki}.")

if __name__ == "__main__":
    main()
