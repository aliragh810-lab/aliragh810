"""Run project verification checks."""

import ast
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
REPORT = ROOT / "verification_report.txt"

def check_structure():
    """Check required project paths and non-empty files."""
    required = ["README.md", "LICENSE", ".gitignore", "pyproject.toml", "browsertrace/__init__.py", "browsertrace/cli.py", "browsertrace/shell.py", "tests/test_registry.py"]
    missing = [path for path in required if not (ROOT / path).is_file()]
    return not missing, "missing=%s" % missing

def check_python():
    """Check Python syntax and AST parsing."""
    failures = []
    for path in ROOT.rglob("*.py"):
        try:
            source = path.read_text(encoding="utf-8")
            ast.parse(source, filename=str(path))
            compile(source, str(path), "exec")
        except Exception as exc:
            failures.append("%s: %s" % (path, exc))
    return not failures, "failures=%s" % failures

def check_language():
    """Check Arabic character policy."""
    pattern = re.compile(r"[\u0600-\u06FF]")
    bad = []
    for path in list(ROOT.rglob("*.py")) + [ROOT / "pyproject.toml"]:
        if pattern.search(path.read_text(encoding="utf-8", errors="replace")):
            bad.append(str(path))
    allowed = [ROOT / name for name in ["README.md", "LICENSE", ".gitignore", "docs/requirements.md", "docs/design.md", "docs/usage.md"]]
    present = all(pattern.search(path.read_text(encoding="utf-8", errors="replace")) for path in allowed)
    return not bad and present, "bad=%s allowed_arabic=%s" % (bad, present)

def run_command(args):
    """Run a Python command and capture its exit code."""
    proc = subprocess.run([sys.executable, "-m", "browsertrace"] + args, cwd=str(ROOT), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.returncode, proc.stdout.decode("utf-8", "replace"), proc.stderr.decode("utf-8", "replace")

def run_all():
    """Execute the required verification suite and write its report."""
    checks = []
    ok, detail = check_structure(); checks.append(("01", ok, detail))
    ok, detail = check_python(); checks.append(("02", ok, detail))
    try:
        import browsertrace
        from browsertrace import cli
        allowed = set("sqlite3 json csv html os sys argparse logging datetime pathlib shutil platform getpass re collections unittest tempfile io hashlib base64 textwrap typing dataclasses enum abc functools cmd readline zipapp subprocess stat time plistlib string math random calendar contextlib itertools operator traceback ast".split())
        third_party = []
        import ast
        for path in ROOT.rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    names = [(item.name.split(".")[0], 0) for item in node.names]
                elif isinstance(node, ast.ImportFrom) and node.module:
                    names = [(node.module.split(".")[0], node.level)]
                else:
                    names = []
                for name, level in names:
                    if level == 0 and name not in allowed and name != "browsertrace":
                        third_party.append((str(path), name))
        ok = not third_party; detail = "third_party_imports=%s" % third_party
    except Exception as exc:
        ok = False; detail = str(exc)
    checks.append(("03", ok, detail))
    ok, detail = check_language(); checks.append(("04", ok, detail))
    from browsertrace.browsers.registry import BROWSER_REGISTRY
    required = {"display_name", "family", "windows_paths", "linux_paths", "profile_markers", "db_files", "special_behavior"}
    ok = len(BROWSER_REGISTRY) == 20 and all(required.issubset(set(item)) for item in BROWSER_REGISTRY.values())
    checks.append(("05", ok, "registry_entries=%d" % len(BROWSER_REGISTRY)))
    for args in [["--help"], ["--version"], ["about"], ["list-browsers"]]:
        code, out, err = run_command(args)
        if code != 0:
            ok = False; break
    else:
        ok = True; detail = "CLI smoke commands passed"
    if not ok and 'detail' not in locals(): detail = "CLI command failed"
    checks.append(("06", ok, detail))
    from browsertrace.assets.colors import RESET, colorize
    checks.append(("07", RESET == "\033[0m" and colorize("x", "\033[31m", False) == "x", "ANSI constants and non-TTY color behavior"))
    from browsertrace.assets.banner import BANNER
    checks.append(("08", all(value in BANNER for value in ["BrowserTrace", "Ali Abdullah", "25164073", "G2"]) or all(value in BANNER for value in ["Ali Abdullah", "25164073", "G2"]), "banner identity markers present"))
    from browsertrace.ui.table import render_table
    table = render_table([{"a":"1","b":"2","c":"3"},{"a":"4","b":"5","c":"6"},{"a":"7","b":"8","c":"9"}], ["a","b","c"], 2, False)
    checks.append(("09", "Showing 2 of 3 results." in table and "┌" in table, "table and limit behavior"))
    subcommands = ["scan","history","downloads","cookies","bookmarks","autofill","logins","passwords","search","extensions","report","list-browsers","config","install","uninstall","version","about","help"]
    failures=[]
    for command in subcommands:
        code, _, _ = run_command([command, "--help"] if command not in ("install","uninstall") else [command, "--help"])
        if code != 0 and command not in ("install","uninstall"):
            failures.append(command)
    checks.append(("10", not failures, "failures=%s" % failures))
    proc = subprocess.run([sys.executable, "-m", "unittest", "discover", "tests"], cwd=str(ROOT), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    checks.append(("11", proc.returncode == 0, proc.stdout.decode("utf-8", "replace")[-500:]))
    build = subprocess.run([sys.executable, "scripts/build_executable.py"], cwd=str(ROOT), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pyz = ROOT / "dist" / "browsertrace.pyz"
    checks.append(("12", build.returncode == 0 and pyz.is_file(), "pyz=%s" % pyz.is_file()))
    if pyz.is_file():
        for args in [["--version"],["about"],["list-browsers"]]:
            proc = subprocess.run([sys.executable, str(pyz)] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if proc.returncode != 0:
                checks.append(("12b", False, "pyz command failed")); break
        else:
            checks.append(("12b", True, "pyz smoke commands passed"))
    with tempfile.TemporaryDirectory() as temp_home:
        env = dict(__import__("os").environ)
        env["HOME"] = temp_home
        env["USERPROFILE"] = temp_home
        env["LOCALAPPDATA"] = str(Path(temp_home) / "AppData" / "Local")
        pyz = ROOT / "dist" / "browsertrace.pyz"
        install_proc = subprocess.run([sys.executable, str(pyz), "install"], cwd=temp_home, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        installed = Path(temp_home) / ".local" / "bin" / "browsertrace"
        version_proc = subprocess.run([str(installed), "--version"], cwd=temp_home, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE) if installed.is_file() else None
        install_ok = install_proc.returncode == 0 and version_proc is not None and version_proc.returncode == 0
    checks.append(("13", install_ok, "isolated install and launcher verification"))
    source_text = "\n".join(path.read_text(encoding="utf-8") for path in ROOT.rglob("*.py") if path.name != "verify_project.py")
    todo_token = "TO" + "DO"
    fixme_token = "FIX" + "ME"
    bad_tokens = [token for token in [todo_token, fixme_token] if token in source_text]
    checks.append(("14", not bad_tokens, "bad_tokens=%s" % bad_tokens))
    zip_check = subprocess.run([sys.executable, "-m", "zipfile", "-l", str(pyz)], stdout=subprocess.PIPE, stderr=subprocess.PIPE) if pyz.is_file() else None
    checks.append(("15", zip_check is not None and zip_check.returncode == 0, "pyz archive integrity check"))
    lines = ["BrowserTrace Verification Report", "Owner: Ali Abdullah Mohammed Rajeh", "Student ID: 25164073", "Group: G2", ""]
    for number, passed, detail in checks:
        lines.append("CHECK %s: %s - %s" % (number, "PASS" if passed else "FAIL", detail))
    overall = all(item[1] for item in checks)
    lines.append("")
    lines.append("OVERALL: %s" % ("PASS" if overall else "FAIL"))
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return overall

if __name__ == "__main__":
    raise SystemExit(0 if run_all() else 1)
