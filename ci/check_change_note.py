"""Fail a PR that changes textkit/ without adding a change note changes/<issue>.md."""
import re
import subprocess
import sys

base = sys.argv[1]
files = subprocess.run(
    ["git", "diff", "--name-only", "--diff-filter=AM", f"{base}...HEAD"],
    check=True, capture_output=True, text=True,
).stdout.split()
if any(f.startswith("textkit/") for f in files) and not any(
    re.fullmatch(r"changes/\d+\.md", f) for f in files
):
    print("A PR that changes textkit/ must add a change note changes/<issue-number>.md "
          "(one line describing the change).")
    sys.exit(1)
print("change note present or not required")
