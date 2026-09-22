"""Scanner tests."""

import unittest
from browsertrace.core.scanner import discover_browsers

class ScannerTests(unittest.TestCase):
    """Verify scanner output type."""
    def test_returns_dict(self):
        """Verify discovery returns a dictionary."""
        self.assertIsInstance(discover_browsers(), dict)
