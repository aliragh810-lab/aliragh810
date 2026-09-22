"""UI color tests."""

import unittest
from browsertrace.assets.colors import RESET, colorize

class ColorTests(unittest.TestCase):
    """Verify ANSI reset and disabled behavior."""
    def test_reset(self):
        """Verify reset code."""
        self.assertEqual(RESET, "\033[0m")
    def test_disabled(self):
        """Verify disabled colors return plain text."""
        self.assertEqual(colorize("x", "\033[31m", False), "x")
