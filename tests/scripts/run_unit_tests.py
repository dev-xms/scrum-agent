#!/usr/bin/env python3
"""Run pytest unit tests for a given BKI. Optionally save artifact to results folder."""
import subprocess
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: run_unit_tests.py <BKI-ID|regression> [sprint-folder]")
        sys.exit(1)

    bki = sys.argv[1].upper().replace("-", "_")
    sprint_folder = sys.argv[2] if len(sys.argv) >= 3 else None

    if bki == "REGRESSION":
        test_path = "tests/"
        artifact_name = "regression_unit.txt"
    else:
        test_path = f"tests/test_{bki}.py"
        artifact_name = f"{sys.argv[1].upper()}_unit.txt"

    cmd = ["python3", "-m", "pytest", test_path, "-v", "--tb=short"]

    if sprint_folder:
        artifact_dir = Path(f"tests/results/{sprint_folder}")
        artifact_dir.mkdir(parents=True, exist_ok=True)
        artifact_path = artifact_dir / artifact_name
        result = subprocess.run(cmd, capture_output=True, text=True)
        artifact_path.write_text(result.stdout + result.stderr)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        sys.exit(result.returncode)
    else:
        result = subprocess.run(cmd, capture_output=False)
        sys.exit(result.returncode)


if __name__ == "__main__":
    main()
