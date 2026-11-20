"""Pemilih menu dengan tombol panah, tanpa paket tambahan. Kembali ke input biasa bila tidak didukung."""
import os
import sys

from . import ui
from .banner import TOOLS as BANNER_TOOLS
from .i18n import TEXT
from .ui import c

ORDER = ["scan", "check", "leads", "gmaps"]
QUIT = ("q", "quit", "exit", "keluar")


def _read_key():
    if os.name == "nt":
        import msvcrt
        ch = msvcrt.getwch()
        if ch in ("\x00", "\xe0"):
            return {"H": "up", "P": "down"}.get(msvcrt.getwch(), "")
        if ch == "\x03":
            raise KeyboardInterrupt
        return {"\r": "enter", "\x1b": "esc"}.get(ch, ch.lower())
    import termios
    import tty
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == "\x1b":
            return {"[A": "up", "[B": "down"}.get(sys.stdin.read(2), "esc")
        if ch == "\x03":
            raise KeyboardInterrupt
        return {"\r": "enter", "\n": "enter"}.get(ch, ch.lower())
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def _fallback(t):
    choice = input("\n" + t["choose"]).strip().lower()
    if not choice or choice in QUIT:
        return "quit"
    if choice in ("l", "links"):
        return "links"
    if choice.isdigit() and 1 <= int(choice) <= 4:
        return ORDER[int(choice) - 1]
    return choice


def pick(lang):
    t = TEXT[lang]
    if not sys.stdin.isatty() or not ui._ENABLED or os.environ.get("VULPFEST_SIMPLE_MENU"):
        return _fallback(t)
    items = [(str(i + 1), key, name) for i, (key, name, _) in enumerate(BANNER_TOOLS)]
    items += [("L", "links", t["item_links"]), ("Q", "quit", t["item_quit"])]
    idx = 0
    out = sys.stdout

    def draw(first):
        if not first:
            out.write(f"\033[{len(items) + 1}A")
        for i, (k, _, label) in enumerate(items):
            selected = i == idx
            mark = c("›", "fox", "bold") if selected else " "
            text = c(label, "bold", "white") if selected else c(label, "gray")
            out.write(f"\r  {mark} {c(k, 'cyan')}  {text}\033[K\n")
        out.write(f"\r  {c(t['pick_hint'], 'gray')}\033[K\n")
        out.flush()

    out.write("\n")
    draw(True)
    while True:
        key = _read_key()
        if key == "up":
            idx = (idx - 1) % len(items)
        elif key == "down":
            idx = (idx + 1) % len(items)
        elif key == "enter":
            return items[idx][1]
        elif key == "esc":
            return "quit"
        else:
            match = next((val for k, val, _ in items if key == k.lower()), None)
            if match:
                return match
            continue
        draw(False)
