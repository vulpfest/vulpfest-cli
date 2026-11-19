"""Ubah logo SVG Vulpfest (vulpfest-mark) menjadi karakter blok untuk terminal.
Bentuk diambil dari path SVG asli: telinga Sigma, V, dan percikan. Jalankan ulang bila logo berubah."""
import re
from pathlib import Path

from PIL import Image, ImageDraw

PATHS = [
    "M5 3 L158 112 L158 138 L32 38 C25 85 46 132 84 176 L90 198 C10 142 -8 70 5 3 Z",
    "M315 3 L162 112 L162 138 L288 38 C295 85 274 132 236 176 L230 198 C310 142 328 70 315 3 Z",
    "M80 164 L160 284 L240 164 L216 158 L160 240 L104 158 Z",
    "M160 70 Q163 84 176 88 Q163 92 160 106 Q157 92 144 88 Q157 84 160 70 Z",
]
VB_X, VB_Y, VB_W, VB_H = -10, 0, 340, 290
COLS = 36   # lebar logo dalam kolom terminal
SS = 8      # supersampling agar tepi halus


def flatten(d, steps=24):
    t = re.findall(r"[MLCQZ]|-?\d+(?:\.\d+)?", d)
    i, cmd, cur, pts = 0, None, (0.0, 0.0), []

    def num():
        nonlocal i
        i += 1
        return float(t[i - 1])

    while i < len(t):
        if t[i] in "MLCQZ":
            cmd = t[i]
            i += 1
            if cmd == "Z":
                continue
        if cmd == "M":
            cur = (num(), num()); pts.append(cur); cmd = "L"
        elif cmd == "L":
            cur = (num(), num()); pts.append(cur)
        elif cmd == "C":
            p1, p2, p3 = (num(), num()), (num(), num()), (num(), num())
            p0 = cur
            for k in range(1, steps + 1):
                s = k / steps
                a, b, c, e = (1 - s) ** 3, 3 * (1 - s) ** 2 * s, 3 * (1 - s) * s * s, s ** 3
                pts.append((a * p0[0] + b * p1[0] + c * p2[0] + e * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + e * p3[1]))
            cur = p3
        elif cmd == "Q":
            p1, p2 = (num(), num()), (num(), num())
            p0 = cur
            for k in range(1, steps + 1):
                s = k / steps
                a, b, c = (1 - s) ** 2, 2 * (1 - s) * s, s * s
                pts.append((a * p0[0] + b * p1[0] + c * p2[0], a * p0[1] + b * p1[1] + c * p2[1]))
            cur = p2
        else:
            i += 1
    return pts


def render():
    w = COLS
    h = round(COLS * VB_H / VB_W)
    h += h % 2
    img = Image.new("L", (w * SS, h * SS), 0)
    dr = ImageDraw.Draw(img)
    sx, sy = w * SS / VB_W, h * SS / VB_H
    for d in PATHS:
        dr.polygon([((x - VB_X) * sx, (y - VB_Y) * sy) for x, y in flatten(d)], fill=255)
    px = img.resize((w, h), Image.BOX).load()
    on = lambda x, y: px[x, y] > 80
    lines = []
    for r in range(0, h, 2):
        row = ""
        for x in range(w):
            top, bot = on(x, r), on(x, r + 1)
            row += "\u2588" if top and bot else "\u2580" if top else "\u2584" if bot else " "
        lines.append(row)
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


if __name__ == "__main__":
    lines = render()
    out = Path(__file__).resolve().parents[1] / "src" / "vulpfest" / "logo.py"
    body = "\n".join(f"    {l!r}," for l in lines)
    out.write_text('"""Dibuat otomatis oleh tools/make_logo.py dari path SVG logo Vulpfest."""\n'
                   f"LOGO = [\n{body}\n]\n", encoding="utf-8")
    print("\n".join(lines))