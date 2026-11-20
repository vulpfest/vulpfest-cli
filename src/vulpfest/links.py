"""Tautan resmi Vulpfest (sama dengan halaman About di vulpfest.com)."""
from .i18n import TEXT
from .ui import c

LINKS = [
    ("Website", "https://www.vulpfest.com"),
    ("Lab", "https://lab.vulpfest.com"),
    ("Journal", "https://journal.vulpfest.com"),
    ("Email", "hello@vulpfest.com"),
    ("GitHub", "https://github.com/vulpfest"),
    ("Instagram", "https://www.instagram.com/vulpfest"),
    ("Threads", "https://www.threads.com/@vulpfest"),
    ("X", "https://x.com/Vulpfest"),
    ("LinkedIn", "https://www.linkedin.com/company/vulpfest"),
    ("Discord", "https://discord.gg/v63BFN7fNc"),
    ("Telegram", "https://t.me/Vulpfest"),
]


def render_links(lang="en"):
    t = TEXT.get(lang, TEXT["en"])
    width = max(len(name) for name, _ in LINKS)
    lines = ["", c(t["links_title"], "fox", "bold"), c("─" * 34, "gray")]
    lines += [f"  {c(name.ljust(width), 'bold', 'white')}  {c(url, 'cyan')}" for name, url in LINKS]
    lines += ["", c(t["links_note"], "gray")]
    return "\n".join(lines)