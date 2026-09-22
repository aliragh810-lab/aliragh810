"""Credential export tests."""

import unittest
import tempfile
from browsertrace.core.credential_export import export_encrypted_credentials

class CredentialExportTests(unittest.TestCase):
    """Verify safe credential export behavior."""
    def test_empty_export(self):
        """Verify missing databases produce an empty evidence file."""
        with tempfile.TemporaryDirectory() as directory:
            path, count = export_encrypted_credentials("chrome", "chromium", directory, directory)
            self.assertTrue(path.is_file())
            self.assertEqual(count, 0)
