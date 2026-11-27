import contextlib
import io
from pathlib import Path
import runpy
import subprocess
import unittest
from unittest.mock import patch


CHECK_SCRIPT = Path(__file__).resolve().parents[1] / "ci" / "check_change_note.py"


class ChangeNoteTest(unittest.TestCase):
    def run_check(self, files):
        output = io.StringIO()
        result = subprocess.CompletedProcess([], 0, stdout="\n".join(files))
        with patch("sys.argv", [str(CHECK_SCRIPT), "origin/main"]), patch(
            "subprocess.run", return_value=result
        ) as git_diff, contextlib.redirect_stdout(output):
            try:
                runpy.run_path(str(CHECK_SCRIPT), run_name="__main__")
            except SystemExit as error:
                status = error.code
            else:
                status = 0
        git_diff.assert_called_once_with(
            ["git", "diff", "--name-only", "--diff-filter=AM", "origin/main...HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
        return status, output.getvalue()

    def test_first_push_without_change_note_fails(self):
        status, output = self.run_check(
            ["textkit/__init__.py", "tests/test_change_note.py"]
        )
        self.assertEqual(status, 1)
        self.assertIn("must add a change note", output)

    def test_followup_with_change_note_passes(self):
        status, output = self.run_check(
            ["textkit/__init__.py", "tests/test_change_note.py", "changes/13.md"]
        )
        self.assertEqual(status, 0)
        self.assertIn("change note present or not required", output)

    def test_invalid_change_note_does_not_satisfy_check(self):
        for note in ("changes/README.md", "changes/issue-13.md", "changes/13.txt"):
            with self.subTest(note=note):
                status, _ = self.run_check(["textkit/core.py", note])
                self.assertEqual(status, 1)

    def test_changes_outside_package_do_not_require_note(self):
        status, _ = self.run_check(["tests/test_core.py", "README.md"])
        self.assertEqual(status, 0)

    def test_no_changes_do_not_require_note(self):
        status, _ = self.run_check([])
        self.assertEqual(status, 0)
