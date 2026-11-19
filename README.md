<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/npm/@vulpfest/icons@0.3/svg/vulpfest-logo-night.svg">
    <img src="https://cdn.jsdelivr.net/npm/@vulpfest/icons@0.3/svg/vulpfest-logo-day.svg" alt="Vulpfest" width="150">
  </picture>
</p>

# vulpfest

All four free tools from [Vulpfest Lab](https://lab.vulpfest.com) in one terminal command. Type `vulpfest`,
pick a tool from the menu, and run it — on Windows, macOS or Linux.

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

Or install the latest code straight from GitHub:

```bash
pip install "vulpfest[all] @ git+https://github.com/vulpfest/vulpfest-cli"
```

GMaps Scout drives a real browser, so it also needs **Google Chrome** installed.

## Use

```bash
vulpfest                                    # menu: pick a tool by number
vulpfest scan example.com                   # scan your own website
vulpfest scan example.com --repo .          # site + project folder in one report
vulpfest check bca-co-id.xyz                # check a suspicious link
vulpfest leads --roles "software house" --industries "technology" --out leads.csv
vulpfest gmaps "coffee shop in Bali" --limit 20 --out places.xlsx
vulpfest <tool> --help                      # all options of a tool
```

Each tool behaves exactly like its standalone version; the source of each one lives in its own repository:
[Cyber-Web-Scanner](https://github.com/FebriOsht/Cyber-Web-Scanner) ·
[linkcheck](https://github.com/FebriOsht/linkcheck) ·
[leadscout](https://github.com/FebriOsht/leadscout) ·
[gmap-scout](https://github.com/FebriOsht/gmap-scout).

## Responsible use

Scan only websites you own or are authorized to test. Collect only public data, respect each site''s terms,
and follow the data-protection law that applies to you.

## Security

Found a security issue? Please report it privately — see [SECURITY.md](SECURITY.md).

## Support this project

If these free tools help you, you can support their development at
[github.com/FebriOsht#support](https://github.com/FebriOsht#support) (Saweria, PayPal, or crypto).
Only send on the network stated there.

## License

MIT © 2026 Febri Osht (Vulpfest). See [LICENSE](LICENSE).
