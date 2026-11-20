"""Menu gaya neofetch: logo Vulpfest (dibuat dari path SVG asli) di kiri, daftar tools di kanan."""
from . import __version__
from .i18n import TEXT
from .logo import LOGO
from .ui import c, rgb

SAND, ROSE = (243, 222, 186), (232, 165, 152)  # gradasi warna logo
_W = len(LOGO[0])
FOX = [l.ljust(_W) for l in LOGO + ["", "V U L P F E S T".center(_W)]]

# (perintah, nama, butuh paket tambahan?)
TOOLS = [
    ("scan", "Cyber Web Scanner", None),
    ("check", "Scam Check", None),
    ("leads", "LeadScout", "need_leads"),
    ("gmaps", "GMaps Scout", "need_gmaps"),
]


def gradient(line):
    n = max(len(line) - 1, 1)
    out = []
    for i, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        k = i / n
        out.append(rgb(ch, *(round(SAND[j] + (ROSE[j] - SAND[j]) * k) for j in range(3))))
    return "".join(out)


def parts(available, lang="en"):
    """available: kunci tool yang paket tambahannya sudah terpasang."""
    t = TEXT.get(lang, TEXT["en"])
    info = [
        c("Vulpfest Lab", "fox", "bold") + c(f"  v{__version__}", "gray"),
        c("─" * 34, "gray"),
        c(t["tagline"], "white"),
        "",
        c(t["tools"], "bold"),
    ]
    for n, (key, name, need) in enumerate(TOOLS, 1):
        ok = need is None or key in available
        dot = c("●", "green") if ok else c("○", "yellow")
        info.append(f"  {dot} {c(str(n) + '.', 'bold')} {c(name, 'bold', 'white')} " + c(f"(vulpfest {key})", "cyan"))
        info.append("     " + c(t["desc"][key], "gray"))
        if not ok:
            info.append("     " + c(t[need], "yellow"))
    info += [
        "",
        c(t["examples"], "bold") + c("  vulpfest scan example.com", "cyan"),
        " " * (len(t["examples"]) + 2) + c("vulpfest check bca-co-id.xyz", "cyan"),
        c(t["help"], "bold") + c(" vulpfest <tool> --help  ·  vulpfest doctor", "cyan"),
        c(t["menu_links"], "gray"),
        c(t["switch"], "gray"),
    ]
    return [gradient(line) for line in FOX], info


def render_rows(available, lang="en"):
    fox, info = parts(available, lang)
    rows = max(len(fox), len(info))
    return [f"{fox[i] if i < len(fox) else ' ' * _W}   {info[i] if i < len(info) else ''}" for i in range(rows)]


def render(available, lang="en"):
    return "\n".join(render_rows(available, lang))
