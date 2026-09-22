"""CLI tests."""

import unittest
from browsertrace.cli import build_parser

class CLITests(unittest.TestCase):
    """Verify parser behavior."""
    def test_version_flag(self):
        """Verify the version flag is accepted."""
        args = build_parser().parse_args(["--version"])
        self.assertTrue(args.version)
