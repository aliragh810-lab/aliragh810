"""Shell tests."""

import unittest
from browsertrace.shell import SUBCOMMANDS

class ShellTests(unittest.TestCase):
    """Verify shell command registration."""
    def test_core_commands(self):
        """Verify required shell commands exist."""
        for command in ["exit", "help", "banner", "scan", "history"]:
            self.assertIn(command, SUBCOMMANDS)
