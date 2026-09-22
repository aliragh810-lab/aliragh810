"""Registry tests."""

import unittest
from browsertrace.browsers.registry import BROWSER_REGISTRY

class RegistryTests(unittest.TestCase):
    """Verify the central browser registry."""
    def test_exactly_twenty(self):
        """Verify the registry contains twenty entries."""
        self.assertEqual(len(BROWSER_REGISTRY), 20)
    def test_required_keys(self):
        """Verify registry entry schema."""
        required = {"display_name", "family", "windows_paths", "linux_paths", "profile_markers", "db_files", "special_behavior"}
        for item in BROWSER_REGISTRY.values():
            self.assertTrue(required.issubset(item))
