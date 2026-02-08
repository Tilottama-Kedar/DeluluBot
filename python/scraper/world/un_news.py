import requests
from bs4 import BeautifulSoup
from datetime import datetime
import xml.etree.ElementTree as ET

UN_RSS_URL = "https://news.un.org/feed/subscribe/en/news/all/rss.xml"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
}

def fetch_un_world(max_articles=5):
    articles = []

    # Fetch RSS feed
    rss_res = requests.get(UN_RSS_URL, headers=HEADERS, timeout=15)
    rss_res.raise_for_status()

    root = ET.fromstring(rss_res.text)
    items = root.findall(".//item")[:max_articles]

    for item in items:
        try:
            url = item.find("link").text.strip()

            article_res = requests.get(url, headers=HEADERS, timeout=15)
            article_res.raise_for_status()

            page = BeautifulSoup(article_res.text, "html.parser")

            title_tag = page.find("h1")
            body_div = page.find("div", class_="text-formatted")

            if not title_tag or not body_div:
                continue

            title = title_tag.text.strip()
            paragraphs = body_div.find_all("p")

            content = " ".join(p.text.strip() for p in paragraphs)
            content = content.replace("\xa0", " ").strip()

            if len(content) < 300:
                continue

            articles.append({
                "source": "UN News",
                "category": "World",
                "title": title,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "summary": content[:350],
                "content": content,
                "url": url
            })

        except Exception as e:
            print(f"Skipped UN article: {e}")

    return articles


if __name__ == "__main__":
    print("RUNNING UN NEWS SCRAPER (NO lxml)")
    news = fetch_un_world()
    print(f"Fetched {len(news)} articles")
    if news:
        print(news[0])
