"""Perintah `vulpfest`: menu interaktif + menjalankan keempat tools Vulpfest Lab.

  vulpfest                      menu: pilih tool dengan nomor
  vulpfest scan example.com     Cyber Web Scanner
  vulpfest check suspicious.link Scam Check
  vulpfest leads --roles ... --industries ...   LeadScout
  vulpfest gmaps "coffee shop jakarta"          GMaps Scout
"""
import importlib.util
import sys
from pathlib import Path

from . import __version__
from .banner import render

TOOLS_DIR = Path(__file__).resolve().parent / "tools"
TOOLS = {"scan": "scanner", "check": "scamcheck", "leads": "leadscout", "gmaps": "gmapscout"}
ORDER = ["scan", "check", "leads", "gmaps"]
NEEDS = {
    "leads": [("ddgs", "duckduckgo_search"), ("pandas",)],
    "gmaps": [("selenium",), ("webdriver_manager",), ("pandas",)],
}


def _has(names):
    return any(importlib.util.find_spec(n) is not None for n in names)


def available():
    return {k for k, groups in NEEDS.items() if all(_has(g) for g in groups)}


def _utf8():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def run_tool(key, args):
    if key in NEEDS and key not in available():
        print(f'{key} needs extra packages: pip install "vulpfest[{key}]"', file=sys.stderr)
        if key == "gmaps":
            print("GMaps Scout also needs Google Chrome installed.", file=sys.stderr)
        return 2
    tool_dir = TOOLS_DIR / TOOLS[key]
    sys.path.insert(0, str(tool_dir))
    sys.argv = [f"vulpfest {key}"] + list(args)
    spec = importlib.util.spec_from_file_location(f"vulpfest_{TOOLS[key]}_cli", tool_dir / "cli.py")
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        rc = module.main()
    except SystemExit as e:
        if e.code is None:
            return 0
        return e.code if isinstance(e.code, int) else 1
    return rc if isinstance(rc, int) else 0


def interactive():
    print(render(available()))
    try:
        choice = input("\nPilih tool (1-4), Enter untuk keluar: ").strip().lower()
        if not choice:
            return 0
        key = ORDER[int(choice) - 1] if choice.isdigit() and 1 <= int(choice) <= 4 else choice
        if key not in TOOLS:
            print("Pilihan tidak dikenal.")
            return 2
        if key == "scan":
            args = [input("Website (mis. example.com): ").strip()]
        elif key == "check":
            args = [input("Tautan yang ingin diperiksa: ").strip()]
        elif key == "leads":
            args = ["--roles", input("Roles, pisahkan dengan koma: ").strip(),
                    "--industries", input("Industries, pisahkan dengan koma: ").strip()]
        else:
            args = [input("Kata kunci pencarian (mis. coffee shop jakarta): ").strip()]
    except (EOFError, KeyboardInterrupt):
        print()
        return 0
    print()
    return run_tool(key, args)


def main(argv=None):
    _utf8()
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        return interactive() if sys.stdin.isatty() else (print(render(available())) or 0)
    head = argv[0].lower()
    if head in ("-h", "--help", "help", "menu"):
        print(render(available()))
        return 0
    if head in ("-v", "--version", "version"):
        print(f"vulpfest {__version__}")
        return 0
    if head not in TOOLS:
        print(f"Tool tidak dikenal: {argv[0]}\n")
        print(render(available()))
        return 2
    return run_tool(head, argv[1:])


if __name__ == "__main__":
    sys.exit(main())