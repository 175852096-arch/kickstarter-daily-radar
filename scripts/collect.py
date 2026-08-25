import json
import re
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from xml.etree import ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
DATA_FILE = ROOT / "data/projects.json"

def fetch(url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "KickstarterDailyRadar/1.0"}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()

def clean_html(text):
    text = re.sub(r"<[^>]+>", " ", text or "")
    return re.sub(r"\s+", " ", text).strip()

def collect_google_news():
    query = 'site:kickstarter.com/projects Kickstarter'
    url = "https://news.google.com/rss/search?" + urllib.parse.urlencode({
        "q": query,
        "hl": "en-US",
        "gl": "US",
        "ceid": "US:en",
    })
    root = ET.fromstring(fetch(url))
    cutoff = datetime.now(timezone.utc) - timedelta(
        hours=CONFIG.get("lookback_hours", 24)
    )
    items = []
    for item in root.findall(".//item"):
        title = clean_html(item.findtext("title", ""))
        link = item.findtext("link", "")
        description = clean_html(item.findtext("description", ""))
        pub = item.findtext("pubDate", "")
        try:
            published = parsedate_to_datetime(pub).astimezone(timezone.utc)
        except Exception:
            continue
        if published < cutoff:
            continue
        if "kickstarter.com/projects" not in link:
            # Google News may return a redirect URL. Keep the item but mark it as discovery-only.
            pass
        items.append({
            "title": title,
            "link": link,
            "description": description,
            "published": published.isoformat(),
            "source": "Google News RSS"
        })
    return items

def dedupe(items):
    seen = set()
    out = []
    for x in items:
        key = (x["title"].lower(), x["link"])
        if key in seen:
            continue
        seen.add(key)
        out.append(x)
    return out

def main():
    old = []
    if DATA_FILE.exists():
        try:
            old = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except Exception:
            old = []

    new = dedupe(collect_google_news())
    merged = dedupe(new + old)[:500]
    DATA_FILE.write_text(
        json.dumps(merged, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"Discovered {len(new)} new items; stored {len(merged)} total.")

if __name__ == "__main__":
    main()
