import requests
from bs4 import BeautifulSoup
from datetime import datetime

IDRW_RSS = (
    "https://news.google.com/rss/search?"
    "q=site:idrw.org+defence+india&hl=en-IN&gl=IN&ceid=IN:en"
)


def fetch_idrw_defence(max_articles=5):
    articles = []

    headers = {
        "User-Agent": "Mozilla/5.0 (DefenceNewsBot/1.0)"
    }

    try:
        res = requests.get(IDRW_RSS, headers=headers, timeout=15)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "lxml-xml")
        items = soup.find_all("item")

        for item in items[:max_articles]:
            title = item.title.text.strip()
            link = item.link.text.strip()

            summary = ""
            if item.description:
                summary = item.description.text.strip()

            pub_date = ""
            if item.pubDate:
                try:
                    pub_date = datetime.strptime(
                        item.pubDate.text.strip(),
                        "%a, %d %b %Y %H:%M:%S %Z"
                    ).strftime("%Y-%m-%d")
                except:
                    pub_date = datetime.now().strftime("%Y-%m-%d")

            articles.append({
                "source": "IDRW",
                "category": "Defence",
                "title": title,
                "date": pub_date,
                "summary": summary[:350],
                "content": summary,
                "url": link,
            })

    except Exception as e:
        print("IDRW fetch error:", e)

    return articles


if __name__ == "__main__":
    print("RUNNING IDRW DEFENCE SCRAPER")

    news = fetch_idrw_defence()

    print(f"Fetched {len(news)} articles")

    if news:
        print(news[0])
