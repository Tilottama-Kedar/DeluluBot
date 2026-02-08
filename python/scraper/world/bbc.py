# scraper/world/bbc.py

import requests
from bs4 import BeautifulSoup
from datetime import datetime

BBC_WORLD_URL = "https://www.bbc.com/news/world"

def fetch_bbc_world(max_articles=5):
    articles_data = []

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(BBC_WORLD_URL, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Collect article links
    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/news/") and "live" not in href:
            full_url = "https://www.bbc.com" + href
            links.add(full_url)

    for url in list(links)[:max_articles]:
        try:
            art_res = requests.get(url, headers=headers, timeout=10)
            art_soup = BeautifulSoup(art_res.text, "html.parser")

            # Extract title
            title_tag = art_soup.find("h1")
            title = title_tag.text.strip() if title_tag else "No title"

            # Extract all paragraphs
            paragraphs = art_soup.find_all("p")
            content = " ".join(p.text.strip() for p in paragraphs)

            # Use first 300 chars as summary
            summary = content[:300]

            articles_data.append({
                "source": "BBC",
                "category": "World",
                "title": title,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "summary": summary,
                "content": content,
                "url": url
            })

        except Exception as e:
            print(f"Skipped article due to error: {e}")

    return articles_data

# Test run
if __name__ == "__main__":
    news = fetch_bbc_world()
    print(f"Fetched {len(news)} articles")
    if news:
        print(news[0])
