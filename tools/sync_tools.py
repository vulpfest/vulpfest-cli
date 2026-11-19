"""Salin kode terbaru keempat tools dari repo masing-masing ke dalam paket vulpfest.
Jalankan setiap kali salah satu tool diperbarui: python tools/sync_tools.py"""
import shutil
from pathlib import Path

PROJECTS = Path.home() / "Projects"
DEST = Path(__file__).resolve().parents[1] / "src" / "vulpfest" / "tools"
MAP = {
    "scanner": ("Cyber-Web-Scanner", ["cli.py", "scanner.py", "ssrf_guard.py", "deep_web.py", "dns_email.py",
                                      "repo_scan.py", "auth_scan.py", "manual_review.py"]),
    "scamcheck": ("linkcheck", ["cli.py", "checker.py", "ssrf_guard.py"]),
    "leadscout": ("leadscout", ["cli.py", "leadscout_core.py"]),
    "gmapscout": ("gmap-scout", ["cli.py", "gmapscout_core.py"]),
}

for name, (repo, files) in MAP.items():
    target = DEST / name
    target.mkdir(parents=True, exist_ok=True)
    for f in files:
        shutil.copy2(PROJECTS / repo / f, target / f)
    print(f"  ✓ {name}: {len(files)} file dari {repo}")