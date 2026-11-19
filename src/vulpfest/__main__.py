"""Perintah `vulpfest`: menu interaktif + menjalankan keempat tools Vulpfest Lab.

  vulpfest                       menu: pilih tool dengan nomor
  vulpfest --lang id             menu berbahasa Indonesia (atau --lang en)
  vulpfest scan example.com      Cyber Web Scanner
  vulpfest check suspicious.link Scam Check
  vulpfest leads --roles ... --industries ...   LeadScout
  vulpfest gmaps "coffee shop jakarta"          GMaps Scout
"""
import importlib.util
import sys
from pathlib import Path

from . import __version__
from .banner import render
from .i18n import TEXT, detect_lang

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


def run_tool(key, args, lang="en"):
    t = TEXT[lang]
    if key in NEEDS and key not in available():
        print(t["needs_extra"].format(key, key), file=sys.stderr)
        if key == "gmaps":
            print(t["needs_chrome"], file=sys.stderr)
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


def interactive(lang):
    t = TEXT[lang]
    print(render(available(), lang))
    try:
        choice = input("\n" + t["choose"]).strip().lower()
        if not choice:
            return 0
        key = ORDER[int(choice) - 1] if choice.isdigit() and 1 <= int(choice) <= 4 else choice
        if key not in TOOLS:
            print(t["unknown_choice"])
            return 2
        if key == "scan":
            args = [input(t["ask_site"]).strip()]
        elif key == "check":
            args = [input(t["ask_link"]).strip()]
        elif key == "leads":
            args = ["--roles", input(t["ask_roles"]).strip(), "--industries", input(t["ask_industries"]).strip()]
        else:
            args = [input(t["ask_query"]).strip()]
    except (EOFError, KeyboardInterrupt):
        print()
        return 0
    print()
    return run_tool(key, args, lang)


def main(argv=None):
    _utf8()
    argv = list(sys.argv[1:] if argv is None else argv)
    lang = detect_lang()
    if len(argv) >= 2 and argv[0] == "--lang" and argv[1].lower() in TEXT:
        lang, argv = argv[1].lower(), argv[2:]
    t = TEXT[lang]
    if not argv:
        if sys.stdin.isatty():
            return interactive(lang)
        print(render(available(), lang))
        return 0
    head = argv[0].lower()
    if head in ("-h", "--help", "help", "menu"):
        print(render(available(), lang))
        return 0
    if head in ("-v", "--version", "version"):
        print(f"vulpfest {__version__}")
        return 0
    if head not in TOOLS:
        print(t["unknown_tool"].format(argv[0]) + "\n")
        print(render(available(), lang))
        return 2
    return run_tool(head, argv[1:], lang)


if __name__ == "__main__":
    sys.exit(main())
