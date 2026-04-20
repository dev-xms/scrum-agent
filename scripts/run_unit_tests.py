#!/usr/bin/env python3
"""
Gate script: run unit tests and save artifact.
Usage: python3 scripts/run_unit_tests.py BKI-XXX [sprint-folder]
sprint-folder defaults to BKI-XXX if omitted.
"""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script_logger import log_invocation, log_result

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/run_unit_tests.py <BKI-ID> [sprint-folder]")
        sys.exit(1)

    bki = sys.argv[1]
    sprint_folder = sys.argv[2] if len(sys.argv) >= 3 else bki
    log_invocation("run_unit_tests.py", [bki, sprint_folder])
    artifact_dir = f"test-results/{sprint_folder}"
    os.makedirs(artifact_dir, exist_ok=True)
    artifact = f"{artifact_dir}/{bki}_unit.txt"

    cmd = ["npm", "test", "--", "--forceExit"] if os.path.exists("package.json") else ["pytest", "-v"]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    with open(artifact, "w") as out:
        out.write(result.stdout)

    print(result.stdout)
    print(f"\nArtifact saved: {artifact}")

    if result.returncode != 0:
        log_result("run_unit_tests.py", "FAILED", f"tests failed for {bki}")
        print(f"GATE FAILED: Unit tests did not pass for {bki}.")
        sys.exit(1)

    log_result("run_unit_tests.py", "OK", f"tests green for {bki}")
    print(f"GATE PASSED: Unit tests green for {bki}.")

if __name__ == "__main__":
    main()
