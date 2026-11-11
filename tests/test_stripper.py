"""Unit tests for automated-dead-code-stripper."""
import unittest
from automated_dead_code_stripper.stripper import DeadCodeStripper

class TestDeadCodeStripper(unittest.TestCase):
    def setUp(self):
        self.stripper = DeadCodeStripper()

    def test_dead_function_removed(self):
        code = "def dead(): return 42\ndef main(): return 1"
        res = self.stripper.strip_dead_code(code, entry_points=["main"])
        self.assertIn("dead", res.removed_functions)
        self.assertNotIn("def dead", res.cleaned_code)
        self.assertIn("def main", res.cleaned_code)
