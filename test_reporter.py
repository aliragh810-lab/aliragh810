"""Reporter tests."""

import unittest
import tempfile
from pathlib import Path
from browsertrace.reporters.json_report import write_json

class ReporterTests(unittest.TestCase):
    """Verify report writing."""
    def test_json(self):
        """Verify JSON report creation."""
        with tempfile.TemporaryDirectory() as directory:
            path = write_json({"history": [{"url": "https://example.com"}]}, Path(directory) / "report.json")
            self.assertTrue(path.is_file())
