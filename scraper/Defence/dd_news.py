import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime

DD_DEFENCE_RSS = "https://ddnews.gov.in/rss/defence.xml"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-IN,en;q=0.9",
}


def fetch_dd_defence(max_articles=5):
    articles = []

    feed = feedparser.parse(DD_DEFENCE_RSS)

    if not feed.entries:
        return []

    for entry in feed.entries[:max_articles]:
        try:
            title = entry.title
            url = entry.link
            date = (
                entry.published
                if hasattr(entry, "published")
                else datetime.now().strftime("%Y-%m-%d")
            )

            res = requests.get(url, headers=HEADERS, timeout=15)
            if res.status_code != 200:
                continue

            soup = BeautifulSoup(res.text, "html.parser")

            content_div = soup.find("div", class_="field--name-body")
            if not content_div:
                continue

            paragraphs = content_div.find_all("p")
            content = " ".join(
                p.get_text(" ", strip=True) for p in paragraphs
            )

            if len(content) < 300:
                continue

            articles.append({
                "source": "DD News (Govt of India)",
                "category": "Defence",
                "title": title,
                "date": date,
                "summary": content[:350],
                "content": content,
                "url": url,
            })

        except Exception:
            continue

    return articles


# 🔽 THIS IS WHAT YOU WERE MISSING
if __name__ == "__main__":
    print("RUNNING DD NEWS DEFENCE SCRAPER")

    news = fetch_dd_defence()

    print(f"Fetched {len(news)} articles")

    if news:
        print(news[0])
