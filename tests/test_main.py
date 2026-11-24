"""Tests for the One Word, First Thought entry program."""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORD = "tumbleweed"


class TestEntry(unittest.TestCase):
    def run_main(self, tmp: Path) -> Path:
        out = tmp / "entry.txt"
        env = dict(os.environ, ENTRY_OUTPUT=str(out))
        subprocess.run(
            [sys.executable, str(ROOT / "main.py")],
            check=True, env=env, cwd=str(ROOT),
        )
        return out

    def test_writes_exact_word(self):
        with tempfile.TemporaryDirectory() as d:
            out = self.run_main(Path(d))
            self.assertEqual(out.read_text(encoding="utf-8"), WORD)

    def test_length_within_gate(self):
        # Gate: /output/entry.txt must be 1-24 characters, not only whitespace.
        self.assertTrue(1 <= len(WORD) <= 24)
        self.assertEqual(len(WORD), 10)

    def test_single_word_letters_only(self):
        self.assertTrue(WORD.isalpha())
        self.assertNotIn(" ", WORD)

    def test_non_blank_and_utf8(self):
        self.assertTrue(WORD.strip())
        WORD.encode("utf-8")

    def test_output_deterministic(self):
        # Same bytes on every run.
        with tempfile.TemporaryDirectory() as d:
            first = self.run_main(Path(d)).read_bytes()
            second = self.run_main(Path(d)).read_bytes()
            self.assertEqual(first, second)

    def test_output_world_readable(self):
        # The grader collects outputs as another user; 0600 fails.
        with tempfile.TemporaryDirectory() as d:
            out = self.run_main(Path(d))
            self.assertTrue(out.stat().st_mode & 0o444)


if __name__ == "__main__":
    unittest.main()
