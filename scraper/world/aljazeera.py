# scraper/world/aljazeera.py

import requests
from bs4 import BeautifulSoup
from datetime import datetime

ALJAZEERA_WORLD_URL = "https://www.aljazeera.com/news/"

def fetch_aljazeera_world(max_articles=5):
    articles_data = []
    headers = {"User-Agent": "Mozilla/5.0"}

    # Step 1: Get homepage
    res = requests.get(ALJAZEERA_WORLD_URL, headers=headers, timeout=10)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    # Step 2: Collect article links
    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        # only keep article links (avoid video, gallery, or repeats)
        if href.startswith("/news") and href.count("/") > 2:
            full_url = "https://www.aljazeera.com" + href
            links.add(full_url)

    links = list(links)[:max_articles]

    # Step 3: Fetch each article
    for url in links:
        try:
            art_res = requests.get(url, headers=headers, timeout=10)
            art_soup = BeautifulSoup(art_res.text, "html.parser")

            # Title
            title_tag = art_soup.find("h1")
            title = title_tag.text.strip() if title_tag else "No title"

            # Full content: all paragraphs inside article body
            content_div = art_soup.find("div", class_="wysiwyg wysiwyg--all-content css-8ug3w0")
            if content_div:
                paragraphs = content_div.find_all("p")
                content = " ".join(p.text.strip() for p in paragraphs)
            else:
                # fallback: grab all <p> tags
                paragraphs = art_soup.find_all("p")
                content = " ".join(p.text.strip() for p in paragraphs)

            # Summary
            summary = content[:300]

            # Skip if content is too short
            if len(content) < 100:
                continue

            articles_data.append({
                "source": "Al Jazeera",
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


# Test
if __name__ == "__main__":
    news = fetch_aljazeera_world()
    print(f"Fetched {len(news)} articles")
    if news:
        print(news[0])
