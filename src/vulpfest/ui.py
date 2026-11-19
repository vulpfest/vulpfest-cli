"""Warna terminal lintas-OS. Warna mati otomatis bila terminal tidak mendukung (mis. piped/CI)."""
import os
import sys

_ENABLED = (
    sys.stdout.isatty()
    and os.environ.get("NO_COLOR") is None
    and os.environ.get("TERM") != "dumb"
)

# Di Windows modern, aktifkan dukungan ANSI bila perlu.
if _ENABLED and os.name == "nt":
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        pass

_CODES = {
    "reset": "0", "bold": "1", "dim": "2",
    "red": "31", "green": "32", "yellow": "33", "blue": "34",
    "magenta": "35", "cyan": "36", "white": "37", "gray": "90",
    "orange": "38;5;208", "fox": "38;5;202",
}


def c(text, *styles):
    if not _ENABLED or not styles:
        return text
    codes = ";".join(_CODES.get(s, "0") for s in styles)
    return f"\033[{codes}m{text}\033[0m"


def rgb(text, r, g, b):
    if not _ENABLED:
        return text
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"
