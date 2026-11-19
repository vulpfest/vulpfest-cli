"""LeadScout from the command line.

Example:
  python cli.py --roles "software house, IT consultant" --industries "technology" --location "Jakarta" --out prospects.csv
"""
import argparse
import csv
import re
import sys

from leadscout_core import COLUMNS, run_campaign


def split_list(value):
    return [v.strip() for v in value.split(",") if v.strip()]


def main():
    p = argparse.ArgumentParser(description="Research B2B prospects from public search results (Vulpfest Lab).")
    p.add_argument("--roles", required=True, help='comma-separated roles or keywords, e.g. "software house, IT consultant"')
    p.add_argument("--industries", required=True, help='comma-separated industry keywords, e.g. "technology"')
    p.add_argument("--location", default="", help='optional location, e.g. "Jakarta"')
    p.add_argument("--campaign", default="LeadScout", help="campaign name stored with each result")
    p.add_argument("--source", choices=["web", "linkedin"], default="web", help="search the entire web (default) or LinkedIn profiles only")
    p.add_argument("--max", type=int, default=10, help="maximum results per keyword (default 10, up to 50)")
    p.add_argument("--out", metavar="FILE.csv", help="save the results as CSV")
    a = p.parse_args()

    roles, industries = split_list(a.roles), split_list(a.industries)
    if not roles or not industries:
        p.error("--roles and --industries cannot be empty")
    print("Reminder: use public company information responsibly and follow data protection laws.", file=sys.stderr)

    def log(msg):
        print(re.sub(r"<[^>]+>", "", msg).strip(), file=sys.stderr)

    rows = run_campaign(a.campaign, roles, industries, a.location.strip(), a.source, max(1, min(a.max, 50)), log_func=log)
    if a.out:
        with open(a.out, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=COLUMNS)
            w.writeheader()
            w.writerows(rows)
        print(f"Saved {len(rows)} results to {a.out}", file=sys.stderr)
    else:
        for r in rows:
            print(f"{r['Keyword']}\t{r['Page Title']}\t{r['URL']}")
        print(f"\n{len(rows)} results", file=sys.stderr)
    return 0 if rows else 1


if __name__ == "__main__":
    sys.exit(main())
