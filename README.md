<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/npm/@vulpfest/icons@0.3/svg/vulpfest-logo-night.svg">
    <img src="https://cdn.jsdelivr.net/npm/@vulpfest/icons@0.3/svg/vulpfest-logo-day.svg" alt="Vulpfest" width="150">
  </picture>
</p>

# vulpfest

[![PyPI](https://img.shields.io/pypi/v/vulpfest)](https://pypi.org/project/vulpfest/)

All four free tools from [Vulpfest Lab](https://lab.vulpfest.com) in one terminal command. Type `vulpfest`,
pick a tool from the menu, and run it on Windows, macOS or Linux.

| # | Tool | Command | What it does |
|---|---|---|---|
| 1 | Cyber Web Scanner | `vulpfest scan` | Checks your own website: headers, SSL/TLS, exposed files, JavaScript secrets, DNS and email, and (with `--repo`) your project folder |
| 2 | Scam Check | `vulpfest check` | Checks a suspicious link before you click it: fake app downloads, look-alike sites, hidden redirects, phishing forms |
| 3 | LeadScout | `vulpfest leads` | Researches B2B prospects from public search results |
| 4 | GMaps Scout | `vulpfest gmaps` | Turns publicly listed business details into a spreadsheet |

## Install

Requires Python 3.9 or newer.

```bash
pip install vulpfest            # Cyber Web Scanner + Scam Check (light)
pip install "vulpfest[all]"     # adds LeadScout and GMaps Scout
```

Prefer to keep it separate from your other Python packages? Use [pipx](https://pipx.pypa.io):
`pipx install "vulpfest[all]"`. To try the newest code from GitHub:
`pip install "vulpfest[all] @ git+https://github.com/vulpfest/vulpfest-cli"`.

GMaps Scout drives a real browser, so it also needs **Google Chrome** installed.

## The menu

Type `vulpfest` and the menu opens:

- move with the **arrow keys** and press **Enter**, or press **1-4** to pick a tool directly;
- press **L** for the official Vulpfest links, **Q** to quit;
- when a tool finishes, press **Enter** to go back to the menu; **Ctrl+C** stops a running tool and also returns to the menu;
- the menu is in English, or in Indonesian when your system language is Indonesian. Switch any time with
  `vulpfest --lang id` or `vulpfest --lang en`.

## Commands

```bash
vulpfest                                    # open the menu
vulpfest scan example.com                   # scan your own website
vulpfest scan example.com --repo .          # site + project folder in one report
vulpfest check bca-co-id.xyz                # check a suspicious link
vulpfest leads --roles "software house" --industries "technology" --out leads.csv
vulpfest gmaps "coffee shop in Bali" --limit 20 --out places.xlsx
vulpfest <tool> --help                      # all options of a tool
vulpfest links                              # official Vulpfest website and social media
vulpfest doctor                             # check Python, packages, Chrome and internet
vulpfest update                             # update to the latest version
vulpfest config                             # show the results folder
vulpfest completion powershell              # Tab completion script (also bash and zsh)
```

Mistype a command and `vulpfest` suggests the closest one (`vulpfest chek` → *Did you mean: vulpfest check?*).

## Where results are saved

A plain file name such as `places.xlsx` is saved in your **results folder**, whatever folder your terminal is in.
By default that is `Documents/Vulpfest` in your home folder. A path that includes a folder
(for example `D:\Data\places.xlsx`) is used exactly as given.

```bash
vulpfest config                             # show the current results folder
vulpfest config out "D:\Data"               # change it
```

## Tab completion

Type `vulpfest d`, press **Tab**, and it becomes `vulpfest doctor`. To turn it on, add one line to your shell profile:

| Shell | Add this line | To |
|---|---|---|
| PowerShell | `vulpfest completion powershell \| Out-String \| Invoke-Expression` | `$PROFILE` |
| bash | `eval "$(vulpfest completion bash)"` | `~/.bashrc` |
| zsh | `eval "$(vulpfest completion zsh)"` | `~/.zshrc` |

Then open a new terminal.

## Settings

| Variable | Effect |
|---|---|
| `VULPFEST_LANG=en` or `id` | menu language |
| `VULPFEST_OUT=<folder>` | results folder for this session (overrides `vulpfest config out`) |
| `NO_COLOR=1` | no colours |
| `VULPFEST_NO_ANIM=1` | skip the opening animation |
| `VULPFEST_SIMPLE_MENU=1` | type a number instead of using the arrow keys |
| `VULPFEST_NO_UPDATE_CHECK=1` | never check for new versions |
| `VULPFEST_DEBUG=1` | show full error details |

## Privacy

- `vulpfest` does not collect usage data or send anything about you.
- Once a day it asks pypi.org for the latest version number, so it can tell you when an update is available.
  Turn this off with `VULPFEST_NO_UPDATE_CHECK=1`.
- The tools contact only what their checks need: the site or link you give them and public lookup services.
- If something breaks, it shows a link for a GitHub issue. Nothing is sent unless you open that link and submit it
  yourself, and your user name is removed from file paths in the report.
- Your settings are stored on your own computer, in the `.vulpfest` folder in your home folder.

## Troubleshooting

Run `vulpfest doctor`. It checks Python, the packages each tool needs, Google Chrome, your internet connection,
the results folder and your terminal, and tells you how to fix anything that is missing.

## Sources

Each tool behaves exactly like its standalone version; the source of each one lives in its own repository:
[Cyber-Web-Scanner](https://github.com/FebriOsht/Cyber-Web-Scanner) ·
[linkcheck](https://github.com/FebriOsht/linkcheck) ·
[leadscout](https://github.com/FebriOsht/leadscout) ·
[gmap-scout](https://github.com/FebriOsht/gmap-scout).

## Responsible use

Scan only websites you own or are authorized to test. Collect only public data, respect each site's terms,
and follow the data-protection law that applies to you.

## Security

Found a security issue? Please report it privately — see [SECURITY.md](SECURITY.md).

## Support this project

If these free tools help you, you can support their development at
[github.com/FebriOsht#support](https://github.com/FebriOsht#support) (Saweria, PayPal, or crypto).
Only send on the network stated there.

## License

MIT © 2026 Febri Osht (Vulpfest). See [LICENSE](LICENSE).