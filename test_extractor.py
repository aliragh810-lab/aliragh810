"""Extractor tests."""

import unittest
import tempfile
from pathlib import Path
from browsertrace.core.extractor import extract_extensions

class ExtractorTests(unittest.TestCase):
    """Verify safe empty extraction behavior."""
    def test_empty_extensions(self):
        """Verify a missing extension directory returns an empty list."""
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(extract_extensions(directory, "chromium"), [])
