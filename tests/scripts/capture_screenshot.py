#!/usr/bin/env python3
"""Render src/index.html to PNG using macOS qlmanage. No browser automation needed."""
import subprocess
import sys
import shutil
from pathlib import Path


def main():
    if len(sys.argv) < 3:
        print("Usage: capture_screenshot.py <BKI-ID> <sprint-folder>")
        sys.exit(1)

    bki = sys.argv[1].upper()
    sprint_folder = sys.argv[2]
    artifact_dir = Path(f"tests/results/{sprint_folder}")
    artifact_dir.mkdir(parents=True, exist_ok=True)
    screenshot_path = artifact_dir / f"{bki}_ui.png"

    html_path = Path("src/index.html").resolve()
    if not html_path.exists():
        print(f"Error: {html_path} not found")
        sys.exit(1)

    tmp_dir = artifact_dir / "_ql_tmp"
    tmp_dir.mkdir(exist_ok=True)

    result = subprocess.run(
        ["qlmanage", "-t", "-s", "1280", "-o", str(tmp_dir), str(html_path)],
        capture_output=True, text=True,
    )

    # qlmanage outputs file as <name>.png
    generated = list(tmp_dir.glob("*.png"))
    if not generated:
        print(f"qlmanage failed: {result.stderr}")
        shutil.rmtree(tmp_dir, ignore_errors=True)
        sys.exit(1)

    shutil.move(str(generated[0]), str(screenshot_path))
    shutil.rmtree(tmp_dir, ignore_errors=True)
    print(f"Screenshot saved: {screenshot_path}")


if __name__ == "__main__":
    main()
