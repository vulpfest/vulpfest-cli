"""Scam Check from the command line.

Examples:
  python cli.py bca-co-id.xyz
  python cli.py example.com/undangan.apk
  python cli.py suspicious.link --json

Works on Windows, macOS and Linux. Only needs: requests, beautifulsoup4.
Exit codes: 0 no danger found, 1 caution, 2 danger, 3 could not check.
"""
import argparse
import json
import sys

import checker

VERDICT = {
    "danger": ("BAHAYA", "tanda penipuan yang kuat"),
    "warn": ("HATI-HATI", "beberapa hal yang mencurigakan"),
    "clear": ("TIDAK DITEMUKAN TANDA BAHAYA", "tetap waspada"),
    "unknown": ("TIDAK DAPAT DIPERIKSA", "periksa kembali tautannya"),
}
EXIT = {"clear": 0, "warn": 1, "danger": 2, "unknown": 3}


def explain(s):
    c = s.get("code")
    if c in ("download", "download-ext"):
        return f"Mengunduh file aplikasi ({s.get('ext') or s.get('kind')}). Jangan dipasang."
    if c == "brand-impersonation":
        return f"Menyebut \"{s.get('brand')}\" tetapi bukan alamat resminya ({s.get('official')})."
    if c == "credential-form":
        extra = " dan mengirimnya ke domain lain" if s.get("cross_domain_post") else ""
        return f"Meminta data rahasia (sandi/PIN/OTP){extra}."
    if c == "at-symbol":
        return "Memakai tanda @ yang bisa menyembunyikan tujuan sebenarnya."
    if c == "ip-host":
        return "Alamat berupa angka IP, bukan nama domain."
    if c == "punycode":
        return "Memakai huruf non-Latin yang bisa menyamar jadi huruf biasa."
    if c == "new-domain":
        return f"Domain baru dibuat sekitar {s.get('days')} hari lalu."
    if c == "shortener":
        return "Tautan pendek yang menyembunyikan tujuan."
    if c == "redirect-chain":
        return f"Melewati {s.get('hops')} pengalihan sebelum sampai tujuan."
    if c == "redirects-elsewhere":
        return f"Berpindah ke alamat lain: {s.get('to')}."
    if c == "risky-tld":
        return f"Akhiran domain {s.get('tld')} sering dipakai untuk penipuan."
    if c == "no-https":
        return "Tidak memakai HTTPS, data tidak terenkripsi."
    return c


def main():
    ap = argparse.ArgumentParser(description="Periksa sebuah tautan untuk tanda-tanda penipuan (Vulpfest Lab).")
    ap.add_argument("url", help="tautan yang ingin diperiksa, misalnya bca-co-id.xyz")
    ap.add_argument("--json", action="store_true", help="tampilkan hasil mentah sebagai JSON")
    args = ap.parse_args()

    print("Pengingat: periksa tautan yang Anda terima; jangan memindai sistem orang lain tanpa izin.", file=sys.stderr)
    result = checker.analyze(args.url)
    result["verdict"] = checker.verdict(result)
    level = result["verdict"]["level"]

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return EXIT.get(level, 3)

    label, tag = VERDICT.get(level, VERDICT["unknown"])
    mark = {"danger": "[!]", "warn": "[~]", "clear": "[ok]", "unknown": "[?]"}.get(level, "[?]")
    print(f"\n  {mark} {label} - {tag}")
    print(f"  Anda masukkan : {result.get('input')}")
    if result.get("final_url") and result["final_url"] != result.get("input"):
        print(f"  Tujuan akhir  : {result['final_url']}")
    print()
    for i, s in enumerate(result.get("signals", []), 1):
        pre = {"danger": "!", "warn": "~", "info": "-"}.get(s.get("level"), "-")
        print(f"  {pre} {explain(s)}")
    if not result.get("signals"):
        print("  (tidak ada sinyal yang ditemukan)")
    print("\n  Catatan: tidak ada alat yang menjamin tautan 100% aman. Tetap waspada.\n")
    return EXIT.get(level, 3)


if __name__ == "__main__":
    sys.exit(main())