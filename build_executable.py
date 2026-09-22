"""Build the BrowserTrace portable Python zip application."""

from pathlib import Path
import shutil
import tempfile
import zipapp

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

def build():
    """Build browsertrace.pyz and launchers."""
    DIST.mkdir(exist_ok=True)
    target = DIST / "browsertrace.pyz"
    for stale in (target, DIST / "browsertrace", DIST / "browsertrace.bat"):
        if stale.exists():
            stale.unlink()
    with tempfile.TemporaryDirectory() as temp:
        staging = Path(temp) / "app"
        package = staging / "browsertrace"
        shutil.copytree(ROOT / "browsertrace", package)
        (staging / "__main__.py").write_text("from browsertrace.cli import main\n\nif __name__ == \"__main__\":\n    raise SystemExit(main())\n", encoding="utf-8")
        zipapp.create_archive(str(staging), str(target), interpreter="/usr/bin/env python3")
    unix = DIST / "browsertrace"
    unix.write_text("#!/bin/sh\nexec python3 \"$(dirname \"$0\")/browsertrace.pyz\" \"$@\"\n", encoding="utf-8")
    unix.chmod(0o755)
    bat = DIST / "browsertrace.bat"
    bat.write_text('@echo off\r\npython "%~dp0browsertrace.pyz" %*\r\n', encoding="utf-8")
    readme = DIST / "README_USER.txt"
    readme.write_text("BrowserTrace 1.0.0 - Quick Start\n\nOwner: Ali Abdullah Mohammed Rajeh\nStudent ID: 25164073\nGroup: G2\n\nRun: python browsertrace.pyz --version\nScan: python browsertrace.pyz scan\nHistory: python browsertrace.pyz history --browser chrome --limit 20\nReport: python browsertrace.pyz report --format html --output report.html\nInstall: python browsertrace.pyz install\n\nEncrypted credential blobs are preserved only as evidence. No decryption and no network access. Use only with legal authorization.\n", encoding="utf-8")
    return target

if __name__ == "__main__":
    print(build())
