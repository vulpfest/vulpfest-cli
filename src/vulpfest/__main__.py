"""Perintah `vulpfest`: menu interaktif + menjalankan keempat tools Vulpfest Lab.

  vulpfest                       menu: pilih tool dengan nomor
  vulpfest --lang id             menu berbahasa Indonesia (atau --lang en)
  vulpfest scan example.com      Cyber Web Scanner
  vulpfest check suspicious.link Scam Check
  vulpfest leads --roles ... --industries ...   LeadScout
  vulpfest gmaps "coffee shop jakarta"          GMaps Scout
"""
import importlib.util
import os
import re
import shutil
import sys
import time
from pathlib import Path

from . import __version__
from . import ui
from .banner import render, render_rows
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
    before = set(sys.modules)
    sys.path.insert(0, str(tool_dir))
    sys.argv = [f"vulpfest {key}"] + list(args)
    spec = importlib.util.spec_from_file_location(f"vulpfest_{TOOLS[key]}_cli", tool_dir / "cli.py")
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        rc = module.main()
        return rc if isinstance(rc, int) else 0
    except SystemExit as e:
        if e.code is None:
            return 0
        return e.code if isinstance(e.code, int) else 1
    finally:
        # Bersihkan agar tool berikutnya di menu yang sama mulai dari keadaan bersih
        try:
            sys.path.remove(str(tool_dir))
        except ValueError:
            pass
        for name in set(sys.modules) - before:
            if str(getattr(sys.modules.get(name), "__file__", "") or "").startswith(str(TOOLS_DIR)):
                sys.modules.pop(name, None)


def _animate_ok():
    return ui._ENABLED and not os.environ.get("VULPFEST_NO_ANIM")


ANSI = re.compile(r"\x1b\[[0-9;]*m")


def _animate_menu(lang):
    """Animasi ~2 detik: logo dari atas ke bawah, VULPFEST huruf demi huruf, lalu teks di sampingnya."""
    from .banner import FOX, _W, gradient, parts
    _, info = parts(available(), lang)
    rows = max(len(FOX), len(info))
    size = shutil.get_terminal_size((80, 24))
    if size.lines < rows + 2 or size.columns < _W + 3 + max(len(ANSI.sub("", x)) for x in info):
        return False  # jendela terlalu kecil: pakai tampilan biasa
    plain = list(FOX) + [" " * _W] * (rows - len(FOX))
    out = sys.stdout
    for i, line in enumerate(plain):
        if i == len(FOX) - 1:  # tulisan V U L P F E S T, huruf demi huruf
            buf = [" "] * len(line)
            for j, ch in enumerate(line):
                if ch != " ":
                    buf[j] = ch
                    out.write("\r" + gradient("".join(buf)))
                    out.flush()
                    time.sleep(0.05)
            out.write("\n")
        else:
            out.write(gradient(line) + "\n")
            out.flush()
            time.sleep(0.035)
    out.write(f"\033[{rows}A")  # kembali ke baris pertama, lalu tulis teks di samping logo
    for i in range(rows):
        right = info[i] if i < len(info) else ""
        out.write(f"\r{gradient(plain[i])}   {right}\033[K\n")
        out.flush()
        time.sleep(0.045)
    return True


def show_menu(lang, animate=False):
    try:
        if animate and _animate_ok() and _animate_menu(lang):
            return
    except KeyboardInterrupt:
        print("\033[0m")
        raise SystemExit(0)
    print(render(available(), lang))


def _ask_args(key, t):
    """Tanya isian tool. None bila isian wajib kosong (kembali ke menu)."""
    if key == "scan":
        v = input(t["ask_site"]).strip()
        return [v] if v else None
    if key == "check":
        v = input(t["ask_link"]).strip()
        return [v] if v else None
    if key == "leads":
        roles = input(t["ask_roles"]).strip()
        industries = input(t["ask_industries"]).strip()
        if not roles or not industries:
            return None
        args = ["--roles", roles, "--industries", industries]
    else:
        query = input(t["ask_query"]).strip()
        if not query:
            return None
        args = [query]
    out = input(t["ask_out_" + key]).strip()
    return args + (["--out", out] if out else [])


QUIT = ("q", "quit", "exit", "keluar")


def interactive(lang):
    t = TEXT[lang]
    first = True
    while True:
        show_menu(lang, animate=first)
        first = False
        try:
            choice = input("\n" + t["choose"]).strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not choice or choice in QUIT:
            return 0
        key = ORDER[int(choice) - 1] if choice.isdigit() and 1 <= int(choice) <= 4 else choice
        if key not in TOOLS:
            print(t["unknown_choice"] + "\n")
            continue
        try:
            args = _ask_args(key, t)
        except (EOFError, KeyboardInterrupt):
            print("\n")
            continue
        if args is None:
            print()
            continue
        print()
        try:
            run_tool(key, args, lang)
        except KeyboardInterrupt:
            print("\n" + t["stopped"])
        try:
            again = input("\n" + t["again"]).strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if again in QUIT:
            return 0
        print()

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
