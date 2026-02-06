import requests
from bs4 import BeautifulSoup
from datetime import datetime

DD_DEFENCE_RSS = (
    "https://news.google.com/rss/search?"
    "q=site:ddnews.gov.in+defence+India&hl=en-IN&gl=IN&ceid=IN:en"
)


def fetch_dd_defence(max_articles=5):
    articles = []

    res = requests.get(DD_DEFENCE_RSS, timeout=15)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "xml")
    items = soup.find_all("item")

    for item in items[:max_articles]:
        title = item.title.text.strip()
        link = item.link.text.strip()
        summary = item.description.text.strip()

        pub_date = item.pubDate.text.strip()
        try:
            pub_date = datetime.strptime(
                pub_date, "%a, %d %b %Y %H:%M:%S %Z"
            ).strftime("%Y-%m-%d")
        except:
            pub_date = datetime.now().strftime("%Y-%m-%d")

        articles.append({
            "source": "DD News",
            "category": "Defence",
            "title": title,
            "date": pub_date,
            "summary": summary[:350],
            "content": summary,
            "url": link,
        })

    return articles


if __name__ == "__main__":
    print("RUNNING DD NEWS DEFENCE SCRAPER")

    news = fetch_dd_defence()

    print(f"Fetched {len(news)} articles")

    if news:
        print(news[0])