"""Cek versi baru di PyPI (sehari sekali, di latar belakang) dan perintah `vulpfest update`."""
import json
import os
import subprocess
import sys
import threading
import time
import urllib.request

from . import __version__
from .config import save_state, state

PYPI = "https://pypi.org/pypi/vulpfest/json"
DAY = 24 * 3600


def _ver(value):
    parts = []
    for piece in str(value).split("."):
        digits = "".join(ch for ch in piece if ch.isdigit())
        parts.append(int(digits) if digits else 0)
    return tuple(parts)


def newer(latest, current=__version__):
    return bool(latest) and _ver(latest) > _ver(current)


def fetch_latest(timeout=3):
    try:
        with urllib.request.urlopen(PYPI, timeout=timeout) as resp:
            return json.load(resp)["info"]["version"]
    except Exception:
        return None


def _refresh():
    latest = fetch_latest()
    save_state({"last_check": time.time(), **({"latest": latest} if latest else {})})


def check_in_background():
    """Versi terbaru yang sudah diketahui dari cek sebelumnya; segarkan di latar belakang bila lewat sehari."""
    if os.environ.get("VULPFEST_NO_UPDATE_CHECK"):
        return None
    current = state()
    if time.time() - current.get("last_check", 0) > DAY:
        threading.Thread(target=_refresh, daemon=True).start()
    latest = current.get("latest")
    return latest if newer(latest) else None


def install_kind():
    if "pipx" in sys.prefix.lower():
        return "pipx"
    try:
        from importlib.metadata import distribution
        raw = distribution("vulpfest").read_text("direct_url.json")
        if raw and json.loads(raw).get("dir_info", {}).get("editable"):
            return "dev"
    except Exception:
        pass
    return "pip"


def run_update(t):
    kind = install_kind()
    if kind == "dev":
        print(t["update_dev"])
        return 0
    if kind == "pipx":
        print(t["update_pipx"])
        return 0
    latest = fetch_latest()
    if latest is None:
        print(t["update_offline"])
        return 2
    if not newer(latest):
        print(t["update_latest"].format(__version__))
        return 0
    print(t["update_running"])
    rc = subprocess.call([sys.executable, "-m", "pip", "install", "--upgrade", "vulpfest"])
    if rc == 0:
        save_state({"latest": latest, "last_check": time.time()})
        print(t["update_done"])
    else:
        print(t["update_failed"])
    return rc
