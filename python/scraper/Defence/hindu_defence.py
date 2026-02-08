import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import time

RSS_URL = (
    "https://news.google.com/rss/search?"
    "q=site:thehindu.com+defence+India&hl=en-IN&gl=IN&ceid=IN:en"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def extract_real_url(item):
    """Extract actual article URL from Google RSS description"""
    if item.description:
        soup = BeautifulSoup(item.description.text, "html.parser")
        a = soup.find("a")
        if a and a.get("href"):
            return a["href"]

    return item.link.text.strip()


def fetch_article_text(url: str):
    """Try to fetch full Hindu article text"""
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        res.raise_for_status()
    except Exception:
        return None

    soup = BeautifulSoup(res.text, "lxml")

    selectors = [
        "div[itemprop='articleBody'] p",
        "div.story-element p",
        "div.articlebodycontent p",
        "section.article-body p",
        "div.content-body p",
        "article p",
    ]

    for sel in selectors:
        paragraphs = soup.select(sel)
        if paragraphs:
            text = " ".join(p.get_text(strip=True) for p in paragraphs)
            if len(text) > 80:  # light sanity check
                return text

    return None


def fetch_hindu_defence(max_articles=5):
    articles = []

    res = requests.get(RSS_URL, headers=HEADERS, timeout=15)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "lxml-xml")
    items = soup.find_all("item")

    for item in items[:max_articles]:
        title = re.sub(r"\s+-\s+thehindu\.com$", "", item.title.text.strip())

        pub_date = item.pubDate.text.strip()
        try:
            pub_date = datetime.strptime(
                pub_date, "%a, %d %b %Y %H:%M:%S %Z"
            ).strftime("%Y-%m-%d")
        except Exception:
            pub_date = datetime.now().strftime("%Y-%m-%d")

        real_url = extract_real_url(item)

        # Try full scrape
        content = fetch_article_text(real_url)

        # Fallback → RSS summary
        if not content and item.description:
            content = BeautifulSoup(
                item.description.text, "html.parser"
            ).get_text(strip=True)

        if not content:
            continue

        articles.append({
            "source": "The Hindu",
            "category": "Defence",
            "title": title,
            "date": pub_date,
            "summary": content[:350],
            "content": content,
            "url": real_url,
        })

        time.sleep(1)

    return articles


if __name__ == "__main__":
    print("RUNNING THE HINDU DEFENCE SCRAPER (REAL CONTENT VERSION)")

    news = fetch_hindu_defence()

    print(f"Fetched {len(news)} articles")

    if news:
        print(news[0])
