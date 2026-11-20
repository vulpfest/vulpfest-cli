"""Pesan error yang ramah dan tautan laporan ke GitHub Issues (teksnya bisa ditinjau sebelum dikirim)."""
import os
import platform
import sys
import traceback
import urllib.parse
from pathlib import Path

from . import __version__

ISSUES = "https://github.com/vulpfest/vulpfest-cli/issues/new"


def report(exc, where, t):
    if os.environ.get("VULPFEST_DEBUG"):
        traceback.print_exception(type(exc), exc, exc.__traceback__)
    name = type(exc).__name__
    print("\n" + t["err_title"].format(f"{name}: {exc}"), file=sys.stderr)
    tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__)[-6:])
    tb = tb.replace(str(Path.home()), "~")  # jangan bocorkan nama pengguna di jalur file
    body = (
        "**What happened**\n\n(describe what you were doing)\n\n**Details**\n"
        f"- vulpfest {__version__}\n- Python {platform.python_version()}\n"
        f"- {platform.system()} {platform.release()}\n- Tool: {where}\n\n```\n{tb[-1500:]}\n```"
    )
    url = ISSUES + "?" + urllib.parse.urlencode({"title": f"{where}: {name}", "body": body})
    print(t["err_report"], file=sys.stderr)
    print(url, file=sys.stderr)
    if not os.environ.get("VULPFEST_DEBUG"):
        print(t["err_debug"], file=sys.stderr)
