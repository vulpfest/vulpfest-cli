"""`vulpfest doctor`: periksa lingkungan dan beri saran perbaikan."""
import importlib.util
import os
import platform
import shutil
import sys
import tempfile
from pathlib import Path

from . import __version__, ui
from .config import out_dir
from .ui import c
from .update import fetch_latest, install_kind, newer


def _has(*names):
    return any(importlib.util.find_spec(n) is not None for n in names)


def _chrome():
    for name in ("chrome", "google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        if shutil.which(name):
            return shutil.which(name)
    candidates = []
    if os.name == "nt":
        for base in (os.environ.get("ProgramFiles"), os.environ.get("ProgramFiles(x86)"), os.environ.get("LOCALAPPDATA")):
            if base:
                candidates.append(Path(base) / "Google" / "Chrome" / "Application" / "chrome.exe")
    elif sys.platform == "darwin":
        candidates.append(Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"))
    return next((str(p) for p in candidates if p.exists()), None)


def doctor(lang="en"):
    ok, warn, bad = c("✓", "green"), c("!", "yellow"), c("✗", "red")
    rows = []

    def add(mark, label, detail=""):
        rows.append((mark, f"  {mark} {label}" + (c(f"   {detail}", "gray") if detail else "")))

    py_ok = sys.version_info >= (3, 9)
    add(ok if py_ok else bad, f"Python {platform.python_version()}", "" if py_ok else "vulpfest needs Python 3.9 or newer")
    kinds = {"dev": "development install (git)", "pipx": "installed with pipx", "pip": "installed with pip"}
    add(ok, f"vulpfest {__version__}", kinds[install_kind()])
    latest = fetch_latest()
    if latest is None:
        add(warn, "Internet / PyPI", "could not reach pypi.org; tools that need the internet may fail")
    elif newer(latest):
        add(warn, f"Update available: {latest}", "run: vulpfest update")
    else:
        add(ok, "Latest version")
    core = _has("requests") and _has("bs4")
    add(ok if core else bad, "Scanner + Scam Check packages", "" if core else "run: pip install --force-reinstall vulpfest")
    leads = _has("ddgs", "duckduckgo_search") and _has("pandas")
    add(ok if leads else warn, "LeadScout packages", "" if leads else 'run: pip install "vulpfest[leads]"')
    gmaps = _has("selenium") and _has("webdriver_manager") and _has("pandas")
    add(ok if gmaps else warn, "GMaps Scout packages", "" if gmaps else 'run: pip install "vulpfest[gmaps]"')
    chrome = _chrome()
    add(ok if chrome else warn, "Google Chrome (for GMaps Scout)", chrome or "install it from google.com/chrome")
    folder = out_dir()
    try:
        folder.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=folder):
            pass
        add(ok, "Results folder", str(folder))
    except Exception:
        add(bad, "Results folder is not writable", f'{folder}  ->  vulpfest config out "<folder>"')
    add(ok if ui._ENABLED else warn, "Terminal colours", "" if ui._ENABLED else "off (NO_COLOR is set or output is redirected)")
    size = shutil.get_terminal_size((80, 24))
    wide = size.columns >= 100
    add(ok if wide else warn, f"Terminal size {size.columns}x{size.lines}", "" if wide else "make the window at least 100 columns wide for the full menu")

    print("\n" + c("vulpfest doctor", "fox", "bold"))
    print(c("─" * 34, "gray"))
    print("\n".join(line for _, line in rows))
    print()
    return 1 if any(mark == bad for mark, _ in rows) else 0
