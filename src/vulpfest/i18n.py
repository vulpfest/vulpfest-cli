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
        "menu_links": "Official links: vulpfest links  ·  www.vulpfest.com",
        "links_title": "Vulpfest · official links",
        "links_note": "Only trust accounts listed here or on vulpfest.com.",
        "choose": "Choose a tool (1-4), L for links, Enter or q to quit: ",
        "again": "Enter = back to menu, q = quit: ",
        "stopped": "Stopped.",
        "update_available": "New version {} available (you have {}). Update: vulpfest update",
        "update_running": "Updating vulpfest...",
        "update_done": "Done. Run vulpfest again to use the new version.",
        "update_latest": "You already have the latest version ({}).",
        "update_offline": "Could not reach PyPI. Check your internet connection.",
        "update_dev": "This is a development install. Update it with: git pull",
        "update_pipx": "Installed with pipx. Update it with: pipx upgrade vulpfest",
        "update_failed": "Update failed. Close vulpfest, then run: python -m pip install --upgrade vulpfest",
        "saved_dir": "Results folder: {}",
        "config_set": "Results folder set to: {}",
        "err_title": "Something went wrong: {}",
        "err_report": "You can report it here (check the text before sending):",
        "err_debug": "For full details, set VULPFEST_DEBUG=1 and run again.",
        "pick_hint": "Arrow keys + Enter, or press 1-4, L or Q",
        "item_links": "Official links",
        "item_quit": "Quit",
        "comp_hint": "Add this line to your shell profile to enable Tab completion:",
        "ask_out_leads": "Save as CSV (e.g. leads.csv), Enter to skip: ",
        "ask_out_gmaps": "Save as .xlsx or .csv (e.g. cafes.xlsx), Enter to skip: ",
        "unknown_choice": "Unknown choice.",
        "ask_site": "Website (e.g. example.com): ",
        "ask_link": "Link to check: ",
        "ask_roles": "Roles, comma separated: ",
        "ask_industries": "Industries, comma separated: ",
        "ask_query": "Search query (e.g. coffee shop in Bali): ",
        "unknown_tool": "Unknown tool: {}",
        "did_you_mean": "Did you mean: vulpfest {}?",
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
        "menu_links": "Tautan resmi: vulpfest links  ·  www.vulpfest.com",
        "links_title": "Vulpfest · tautan resmi",
        "links_note": "Hanya percayai akun yang tercantum di sini atau di vulpfest.com.",
        "choose": "Pilih tool (1-4), L untuk tautan, Enter atau q untuk keluar: ",
        "again": "Enter = kembali ke menu, q = keluar: ",
        "stopped": "Dihentikan.",
        "update_available": "Versi baru {} tersedia (Anda memakai {}). Perbarui: vulpfest update",
        "update_running": "Memperbarui vulpfest...",
        "update_done": "Selesai. Jalankan vulpfest lagi untuk memakai versi baru.",
        "update_latest": "Anda sudah memakai versi terbaru ({}).",
        "update_offline": "Tidak bisa menghubungi PyPI. Periksa koneksi internet.",
        "update_dev": "Ini instalasi pengembangan. Perbarui dengan: git pull",
        "update_pipx": "Dipasang lewat pipx. Perbarui dengan: pipx upgrade vulpfest",
        "update_failed": "Pembaruan gagal. Tutup vulpfest, lalu jalankan: python -m pip install --upgrade vulpfest",
        "saved_dir": "Folder hasil: {}",
        "config_set": "Folder hasil diubah ke: {}",
        "err_title": "Terjadi kesalahan: {}",
        "err_report": "Anda bisa melaporkannya di sini (periksa teksnya sebelum dikirim):",
        "err_debug": "Untuk detail lengkap, set VULPFEST_DEBUG=1 lalu jalankan lagi.",
        "pick_hint": "Tombol panah + Enter, atau tekan 1-4, L, atau Q",
        "item_links": "Tautan resmi",
        "item_quit": "Keluar",
        "comp_hint": "Tambahkan baris ini ke profil shell Anda untuk mengaktifkan Tab completion:",
        "ask_out_leads": "Simpan sebagai CSV (mis. leads.csv), Enter untuk lewati: ",
        "ask_out_gmaps": "Simpan sebagai .xlsx atau .csv (mis. kafe.xlsx), Enter untuk lewati: ",
        "unknown_choice": "Pilihan tidak dikenal.",
        "ask_site": "Website (mis. example.com): ",
        "ask_link": "Tautan yang ingin diperiksa: ",
        "ask_roles": "Roles, pisahkan dengan koma: ",
        "ask_industries": "Industries, pisahkan dengan koma: ",
        "ask_query": "Kata kunci pencarian (mis. coffee shop jakarta): ",
        "unknown_tool": "Tool tidak dikenal: {}",
        "did_you_mean": "Maksud Anda: vulpfest {}?",
        "needs_extra": '{} perlu paket tambahan: pip install "vulpfest[{}]"',
        "needs_chrome": "GMaps Scout juga perlu Google Chrome terpasang.",
    },
}
