"""Scam Check - analisis tautan di sisi server.

Server yang membuka tautan, bukan perangkat pengguna. JavaScript tidak dijalankan, file tidak
diunduh penuh (hanya header), dan semua permintaan lewat ssrf_guard (menolak alamat internal).
Hasil: daftar sinyal. checker tidak pernah menyatakan sebuah tautan "aman"; penilaian akhir
(bahaya/hati-hati/bersih) dihitung dari bobot sinyal di verdict().
"""
import re
import socket
from datetime import datetime, timezone
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup

from ssrf_guard import BlockedTarget, check_url, guard_session

MAX_REDIRECTS = 8
TIMEOUT = 8

# Merek yang sering ditiru (global + Indonesia). Dipakai untuk mendeteksi domain peniru.
BRANDS = {
    "paypal": ("paypal.com",), "amazon": ("amazon.com",), "apple": ("apple.com", "icloud.com"),
    "microsoft": ("microsoft.com", "live.com", "outlook.com"), "google": ("google.com",),
    "netflix": ("netflix.com",), "facebook": ("facebook.com",), "instagram": ("instagram.com",),
    "whatsapp": ("whatsapp.com",), "binance": ("binance.com",), "coinbase": ("coinbase.com",),
    "metamask": ("metamask.io",), "steam": ("steampowered.com",), "dhl": ("dhl.com",),
    "bca": ("bca.co.id", "klikbca.com"), "mandiri": ("bankmandiri.co.id",), "bri": ("bri.co.id", "bankbri.co.id"),
    "bni": ("bni.co.id",), "dana": ("dana.id",), "ovo": ("ovo.id",), "gopay": ("gopay.co.id",),
    "shopee": ("shopee.co.id", "shopee.com"), "tokopedia": ("tokopedia.com",), "lazada": ("lazada.co.id",),
    "jne": ("jne.co.id",), "jnt": ("jet.co.id",), "sicepat": ("sicepat.com",), "bpjs": ("bpjs-kesehatan.go.id",),
    "prakerja": ("prakerja.go.id",), "pajak": ("pajak.go.id",),
}
BRAND_HOSTS = {h for hosts in BRANDS.values() for h in hosts}

RISKY_TLDS = (".zip", ".mov", ".xyz", ".top", ".tk", ".ml", ".ga", ".cf", ".gq", ".work", ".click",
              ".link", ".rest", ".country", ".kim", ".loan", ".download", ".racing", ".win", ".bid")
SHORTENERS = ("bit.ly", "t.co", "tinyurl.com", "goo.gl", "ow.ly", "is.gd", "buff.ly", "cutt.ly",
              "rebrand.ly", "s.id", "bit.do", "shorturl.at", "rb.gy", "t.ly", "linktr.ee")
DOWNLOAD_EXT = (".apk", ".exe", ".msi", ".bat", ".scr", ".jar", ".dmg", ".apks", ".xapk")
SENSITIVE_WORDS = ("password", "kata sandi", "sandi", "pin", "otp", "cvv", "cvc", "kartu kredit",
                   "card number", "nomor kartu", "mother", "ibu kandung", "nik", "ktp")
# huruf yang sering dipakai menyamar
CONFUSABLE = str.maketrans({"0": "o", "1": "l", "3": "e", "4": "a", "5": "s", "7": "t", "$": "s"})


def normalize(raw):
    raw = (raw or "").strip()
    if not raw:
        return None
    if "://" not in raw:
        raw = "http://" + raw
    return raw


def registered_domain(host):
    host = (host or "").lower().strip(".")
    parts = host.split(".")
    sld = {"co", "or", "go", "ac", "sch", "web", "my", "net", "com", "org"}
    if len(parts) >= 3 and len(parts[-1]) == 2 and parts[-2] in sld:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:]) if len(parts) >= 2 else host


def brand_impersonation(host, full_url):
    """Cari merek yang disebut di domain/subdomain/path tetapi domain terdaftarnya bukan domain resmi."""
    host = (host or "").lower()
    reg = registered_domain(host)
    if reg in BRAND_HOSTS:
        return None  # ini domain resmi
    labels = host.split(".")[:-2] if host.count(".") >= 2 else []
    hay_host = host.translate(CONFUSABLE)
    for brand, official in BRANDS.items():
        # merek muncul sebagai label subdomain, atau nama merek menempel di domain (bca-co-id, klik-bca)
        in_sub = any(brand in lbl.translate(CONFUSABLE) for lbl in labels)
        in_dom = brand in reg.split(".")[0].translate(CONFUSABLE)
        if (in_sub or in_dom) and reg not in official:
            return {"brand": brand, "official": official[0], "found_in": host}
    return None


def is_punycode(host):
    return "xn--" in (host or "").lower()


def _session():
    s = requests.Session()
    s.headers["User-Agent"] = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                               "(KHTML, like Gecko) Chrome/130.0 Safari/537.36 VulpfestScamCheck/1.0")
    s.headers["Accept"] = "text/html,application/xhtml+xml,*/*;q=0.8"
    return guard_session(s, max_redirects=MAX_REDIRECTS)


def follow(url):
    """Ikuti redirect di server. Kembalikan (respons akhir, rantai, error)."""
    s = _session()
    chain, current = [], url
    try:
        for _ in range(MAX_REDIRECTS + 1):
            check_url(current)
            r = s.get(current, timeout=TIMEOUT, allow_redirects=False, verify=True)
            chain.append({"url": current, "status": r.status_code})
            if r.is_redirect or r.is_permanent_redirect:
                loc = r.headers.get("Location", "")
                if not loc:
                    break
                current = urljoin(current, loc)
                continue
            return r, chain, None
        return None, chain, "Terlalu banyak pengalihan (redirect)."
    except BlockedTarget as e:
        return None, chain, str(e)
    except requests.exceptions.SSLError:
        try:
            r = s.get(current, timeout=TIMEOUT, allow_redirects=False, verify=False)
            chain.append({"url": current, "status": r.status_code, "ssl_error": True})
            return r, chain, None
        except requests.exceptions.RequestException as e:
            return None, chain, _err(e)
    except requests.exceptions.RequestException as e:
        return None, chain, _err(e)


def _err(e):
    return f"{e.__class__.__name__}"


def domain_age_days(host):
    """Umur domain via RDAP (data pendaftaran publik). None bila tidak diketahui."""
    reg = registered_domain(host)
    try:
        r = requests.get(f"https://rdap.org/domain/{reg}", timeout=6, headers={"Accept": "application/rdap+json"})
        if r.status_code != 200:
            return None
        for ev in r.json().get("events", []):
            if ev.get("eventAction") == "registration" and ev.get("eventDate"):
                d = datetime.fromisoformat(ev["eventDate"].replace("Z", "+00:00"))
                return (datetime.now(timezone.utc) - d).days
    except (requests.RequestException, ValueError, KeyError):
        return None
    return None


def looks_like_login(resp):
    """Halaman meminta kredensial? (ada input password, atau kata sensitif + input)."""
    ctype = resp.headers.get("Content-Type", "").lower()
    if "html" not in ctype:
        return None
    soup = BeautifulSoup(resp.text[:200000], "html.parser")
    has_password = bool(soup.find("input", attrs={"type": "password"}))
    text = soup.get_text(" ", strip=True).lower()[:5000]
    mentions = [w for w in SENSITIVE_WORDS if w in text]
    forms_post = soup.find_all("form")
    # form mengirim ke domain lain?
    page_host = (urlparse(resp.url).hostname or "").lower()
    cross = []
    for f in forms_post:
        action = (f.get("action") or "").strip()
        if action.startswith(("http://", "https://")):
            ah = (urlparse(action).hostname or "").lower()
            if ah and registered_domain(ah) != registered_domain(page_host):
                cross.append(ah)
    if has_password or (mentions and forms_post):
        return {"password_field": has_password, "sensitive_words": mentions[:5], "cross_domain_post": sorted(set(cross))[:3]}
    return None


def download_kind(resp, final_url):
    cd = resp.headers.get("Content-Disposition", "").lower()
    ctype = resp.headers.get("Content-Type", "").lower()
    path = urlparse(final_url).path.lower()
    ext = next((e for e in DOWNLOAD_EXT if path.endswith(e) or e[1:] in cd), None)
    app_ct = any(x in ctype for x in ("application/vnd.android.package-archive", "application/x-msdownload",
                                      "application/octet-stream", "application/x-apple-diskimage"))
    if ext:
        return ext
    if app_ct and "attachment" in cd:
        return "file aplikasi"
    return None


def analyze(raw_url):
    url = normalize(raw_url)
    out = {"input": raw_url, "url": url, "signals": [], "chain": [], "final_url": None, "error": None}
    if not url:
        out["error"] = "empty"
        return out
    p0 = urlparse(url)
    host0 = (p0.hostname or "").lower()

    def sig(level, code, **extra):
        out["signals"].append({"level": level, "code": code, **extra})

    # --- sinyal dari URL mentah, tanpa koneksi ---
    if "@" in (p0.netloc or ""):
        sig("danger", "at-symbol")
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", host0 or ""):
        sig("warn", "ip-host")
    if is_punycode(host0):
        sig("warn", "punycode", host=host0)
    if host0 in SHORTENERS:
        sig("info", "shortener", host=host0)
    if any(host0.endswith(t) or registered_domain(host0).endswith(t) for t in RISKY_TLDS):
        sig("info", "risky-tld", tld=next(t for t in RISKY_TLDS if host0.endswith(t) or registered_domain(host0).endswith(t)))
    imp0 = brand_impersonation(host0, url)
    if imp0:
        sig("danger", "brand-impersonation", **imp0)
    if any(url.lower().split("?")[0].endswith(e) for e in DOWNLOAD_EXT):
        sig("danger", "download-ext", ext=next(e for e in DOWNLOAD_EXT if url.lower().split('?')[0].endswith(e)))

    # --- buka tautan di server ---
    resp, chain, err = follow(url)
    out["chain"] = chain
    if err:
        out["error"] = err
        return out  # sinyal URL (mis. peniru merek) sudah terkumpul di atas dan tetap dinilai
    out["final_url"] = resp.url
    pf = urlparse(resp.url)
    host_f = (pf.hostname or "").lower()

    if len([c for c in chain if c.get("status", 0) in (301, 302, 303, 307, 308)]) >= 2:
        sig("info", "redirect-chain", hops=len(chain))
    if host_f and registered_domain(host_f) != registered_domain(host0):
        sig("info", "redirects-elsewhere", to=host_f)

    dk = download_kind(resp, resp.url)
    if dk and not any(x["code"] == "download-ext" for x in out["signals"]):
        sig("danger", "download", kind=dk)

    impf = brand_impersonation(host_f, resp.url)
    if impf and impf != imp0:
        sig("danger", "brand-impersonation", **impf)

    if not dk:
        login = looks_like_login(resp)
        if login:
            lvl = "danger" if login["cross_domain_post"] else "warn"
            sig(lvl, "credential-form", **login)

    age = domain_age_days(host_f)
    if age is not None:
        out["domain_age_days"] = age
        if age <= 30:
            sig("warn", "new-domain", days=age)
        elif age <= 180:
            sig("info", "youngish-domain", days=age)

    return out


def verdict(result):
    """Tiga tingkat jujur dari sinyal. Tidak pernah menyatakan 'aman'."""
    sigs = result.get("signals", [])
    if result.get("error") and not any(s["level"] in ("danger", "warn") for s in sigs):
        return {"level": "unknown", "signals": sigs}
    levels = [s["level"] for s in result["signals"]]
    danger = levels.count("danger")
    warn = levels.count("warn")
    info = levels.count("info")
    if danger >= 1:
        level = "danger"
    elif warn >= 1 or info >= 3:
        level = "warn"
    else:
        level = "clear"
    return {"level": level, "counts": {"danger": danger, "warn": warn, "info": info}, "signals": result["signals"]}