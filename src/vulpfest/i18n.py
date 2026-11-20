"""Bahasa menu: Inggris bawaan, Indonesia bila sistem berbahasa Indonesia atau diminta (--lang / VULPFEST_LANG)."""
import locale
import os
import warnings


def detect_lang():
    env = (os.environ.get("VULPFEST_LANG") or "").strip().lower()
    if env in ("en", "id"):
        return env
    if os.name == "nt":
        try:
            import ctypes
            if ctypes.windll.kernel32.GetUserDefaultUILanguage() & 0x3FF == 0x21:  # 0x21 = Indonesian
                return "id"
        except Exception:
            pass
    names = [os.environ.get(v, "") for v in ("LC_ALL", "LC_MESSAGES", "LANG", "LANGUAGE")]
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            names.append(locale.getdefaultlocale()[0] or "")
    except Exception:
        pass
    for n in names:
        n = n.lower()
        if n.startswith("id") or "indonesia" in n:
            return "id"
    return "en"


TEXT = {
    "en": {
        "tagline": "Free tools for web security and scam protection.",
        "tools": "Tools:", "examples": "Examples:", "help": "Help:",
        "need_leads": "needs: pip install vulpfest[leads]",
        "need_gmaps": "needs: pip install vulpfest[gmaps] + Chrome",
        "desc": {
            "scan": "Check your own website (headers, SSL, exposed files, DNS).",
            "check": "Check a suspicious link before you click it.",
            "leads": "Research B2B prospects from public search results.",
            "gmaps": "Turn public business listings into a spreadsheet.",
        },
        "switch": "Bahasa Indonesia: vulpfest --lang id",
        "choose": "Choose a tool (1-4), Enter or q to quit: ",
        "again": "Enter = back to menu, q = quit: ",
        "stopped": "Stopped.",
        "ask_out_leads": "Save as CSV (e.g. leads.csv), Enter to skip: ",
        "ask_out_gmaps": "Save as .xlsx or .csv (e.g. cafes.xlsx), Enter to skip: ",
        "unknown_choice": "Unknown choice.",
        "ask_site": "Website (e.g. example.com): ",
        "ask_link": "Link to check: ",
        "ask_roles": "Roles, comma separated: ",
        "ask_industries": "Industries, comma separated: ",
        "ask_query": "Search query (e.g. coffee shop in Bali): ",
        "unknown_tool": "Unknown tool: {}",
        "needs_extra": '{} needs extra packages: pip install "vulpfest[{}]"',
        "needs_chrome": "GMaps Scout also needs Google Chrome installed.",
    },
    "id": {
        "tagline": "Alat gratis untuk keamanan web dan anti-penipuan.",
        "tools": "Tools:", "examples": "Contoh:", "help": "Bantuan:",
        "need_leads": "perlu: pip install vulpfest[leads]",
        "need_gmaps": "perlu: pip install vulpfest[gmaps] + Chrome",
        "desc": {
            "scan": "Periksa keamanan situs Anda (header, SSL, file bocor, DNS).",
            "check": "Periksa tautan mencurigakan sebelum diklik.",
            "leads": "Riset prospek B2B dari hasil pencarian publik.",
            "gmaps": "Kumpulkan detail bisnis publik ke spreadsheet.",
        },
        "switch": "English: vulpfest --lang en",
        "choose": "Pilih tool (1-4), Enter atau q untuk keluar: ",
        "again": "Enter = kembali ke menu, q = keluar: ",
        "stopped": "Dihentikan.",
        "ask_out_leads": "Simpan sebagai CSV (mis. leads.csv), Enter untuk lewati: ",
        "ask_out_gmaps": "Simpan sebagai .xlsx atau .csv (mis. kafe.xlsx), Enter untuk lewati: ",
        "unknown_choice": "Pilihan tidak dikenal.",
        "ask_site": "Website (mis. example.com): ",
        "ask_link": "Tautan yang ingin diperiksa: ",
        "ask_roles": "Roles, pisahkan dengan koma: ",
        "ask_industries": "Industries, pisahkan dengan koma: ",
        "ask_query": "Kata kunci pencarian (mis. coffee shop jakarta): ",
        "unknown_tool": "Tool tidak dikenal: {}",
        "needs_extra": '{} perlu paket tambahan: pip install "vulpfest[{}]"',
        "needs_chrome": "GMaps Scout juga perlu Google Chrome terpasang.",
    },
}
