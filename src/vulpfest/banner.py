"""Logo rubah Vulpfest (ASCII) dan menu, gaya neofetch: logo di kiri, info di kanan."""
from . import __version__
from .ui import c

# Logo Vulpfest: dibuat dari path SVG asli (telinga Sigma, V, percikan) oleh tools/make_logo.py.
from .logo import LOGO
from .ui import rgb

SAND, ROSE = (243, 222, 186), (232, 165, 152)  # gradasi warna logo
_W = len(LOGO[0])
FOX = [l.ljust(_W) for l in LOGO + ["", "V U L P F E S T".center(_W)]]


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

TOOLS = [
    ("scan",  "Cyber Web Scanner", "Periksa keamanan situs Anda (header, SSL, file bocor, DNS).", "ready"),
    ("check", "Scam Check",        "Periksa tautan mencurigakan sebelum diklik.",                "ready"),
    ("leads", "LeadScout",         "Riset prospek B2B dari hasil pencarian publik.",             "leads"),
    ("gmaps", "GMaps Scout",       "Kumpulkan detail bisnis publik ke spreadsheet.",             "gmaps"),
]

STATUS = {
    "ready": c("siap", "green"),
    "leads": c("perlu: pip install vulpfest[leads]", "yellow"),
    "gmaps": c("perlu: pip install vulpfest[gmaps] + Chrome", "yellow"),
}


def render(available):
    """available: set berisi kunci tool yang dependensinya sudah terpasang."""
    info = []
    info.append(c("Vulpfest Lab", "fox", "bold") + c(f"  v{__version__}", "gray"))
    info.append(c("─" * 34, "gray"))
    info.append(c("Alat gratis untuk keamanan & anti-penipuan.", "white"))
    info.append("")
    info.append(c("Tools:", "bold"))
    for n, (key, name, desc, need) in enumerate(TOOLS, 1):
        ok = need == "ready" or key in available
        dot = c("●", "green") if ok else c("○", "yellow")
        line = f"  {dot} {c(str(n) + '.', 'bold')} {c(name, 'bold', 'white')} " + c(f"(vulpfest {key})", "cyan")
        info.append(line)
        info.append("     " + c(desc, "gray"))
        if not ok:
            info.append("     " + STATUS[need])
    info.append("")
    info.append(c("Contoh:", "bold") + c("  vulpfest scan example.com", "cyan"))
    info.append(c("        vulpfest check bca-co-id.xyz", "cyan"))
    info.append(c("Bantuan:", "bold") + c(" vulpfest <tool> --help", "cyan"))

    fox = [gradient(line) for line in FOX]
    # Sejajarkan logo (kiri) dan info (kanan)
    pad = len(FOX)
    rows = max(len(fox), len(info))
    out = []
    for i in range(rows):
        left = fox[i] if i < len(fox) else " " * len(FOX[0])
        right = info[i] if i < len(info) else ""
        out.append(f"{left}   {right}")
    return "\n".join(out)
