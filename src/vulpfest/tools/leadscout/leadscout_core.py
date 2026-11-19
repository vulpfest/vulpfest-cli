"""LeadScout core: the search logic shared by the Streamlit app (app.py) and the command line (cli.py)."""
import time

try:
    from ddgs import DDGS
except ImportError:
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        DDGS = None

COLUMNS = ["Campaign", "Keyword", "Location", "Page Title", "URL"]


def duckduckgo_search_api(query, max_results=15, target_type='linkedin', log_func=None):
    results = []
    try:
        if DDGS is None:
            raise ImportError("Missing library. Please run: pip install ddgs")
        ddgs = DDGS()
        search_results = ddgs.text(query, max_results=max_results)

        if not search_results:
            if log_func: log_func("<span style='color:#f87171;'>[!] DDG API returned 0 results (Backend Limit Hit).</span>")
            return []

        for r in search_results:
            href = r.get('href', '')
            title = r.get('title', '')

            if target_type == 'linkedin':
                # Strictly filter for LinkedIn Profiles only
                if 'linkedin.com/in/' in href and '/dir/' not in href and '/jobs/' not in href:
                    clean_url = href.split('?')[0]
                    if clean_url not in [x['url'] for x in results]:
                        results.append({'title': title, 'url': clean_url})
            else:
                # Entire Web mode: accept all relevant URLs
                if href not in [x['url'] for x in results]:
                    results.append({'title': title, 'url': href})

        return results
    except Exception as e:
        if log_func: log_func(f"<span style='color:#f87171;'>[!] Internal DDG API error: {str(e)}</span>")
        return []


def build_query(role, industry, location="", target_type="web"):
    location_dork = f' "{location}"' if location else ""
    query = f'"{role}" {industry}{location_dork}'
    return f"{query} site:linkedin.com/in" if target_type == "linkedin" else query


def run_campaign(campaign, roles, industries, location="", target_type="web", max_results=10, log_func=None, delay=1.5):
    """Same search flow as the web app; returns a list of rows with COLUMNS."""
    rows, seen = [], set()
    for role in roles:
        if log_func: log_func(f"[*] Mining data for: {role} ...")
        results = duckduckgo_search_api(build_query(role, industries[0], location, target_type), max_results, target_type, log_func)
        time.sleep(delay)  # respect API limits
        count = 0
        for item in results:
            if count >= max_results:
                break
            if item["url"] in seen:
                continue
            seen.add(item["url"])
            rows.append({"Campaign": campaign, "Keyword": role, "Location": location or "Global",
                         "Page Title": item["title"], "URL": item["url"]})
            if log_func: log_func(f"[+] Found: {item['url']}")
            count += 1
    return rows
