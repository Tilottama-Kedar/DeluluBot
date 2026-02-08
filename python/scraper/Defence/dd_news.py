import requests
from bs4 import BeautifulSoup
from datetime import datetime

DD_DEFENCE_RSS = (
    "https://news.google.com/rss/search?"
    "q=site:ddnews.gov.in+defence+India&hl=en-IN&gl=IN&ceid=IN:en"
)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def fetch_article_body(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        res.raise_for_status()
    except:
        return None

    soup = BeautifulSoup(res.text, "lxml")

    selectors = [
        "div.field-item p",
        "div.article-body p",
        "div.content p",
        "article p"
    ]

    for sel in selectors:
        paragraphs = soup.select(sel)
        if paragraphs:
            text = " ".join(p.get_text(strip=True) for p in paragraphs)
            if len(text) > 80:
                return text

    return None


def extract_real_url(item):
    if item.description:
        soup = BeautifulSoup(item.description.text, "html.parser")
        a = soup.find("a")
        if a and a.get("href"):
            return a["href"]

    return item.link.text.strip()


def fetch_dd_defence(max_articles=5):
    articles = []

    res = requests.get(DD_DEFENCE_RSS, headers=HEADERS, timeout=15)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "xml")
    items = soup.find_all("item")

    for item in items[:max_articles]:
        title = item.title.text.strip()
        link = extract_real_url(item)

        summary_html = item.description.text
        summary = BeautifulSoup(summary_html, "html.parser").get_text(" ", strip=True)

        pub_date = item.pubDate.text.strip()
        try:
            pub_date = datetime.strptime(
                pub_date, "%a, %d %b %Y %H:%M:%S %Z"
            ).strftime("%Y-%m-%d")
        except:
            pub_date = datetime.now().strftime("%Y-%m-%d")

        body = fetch_article_body(link)
        content = body if body else summary

        articles.append({
            "source": "DD News",
            "category": "Defence",
            "title": title,
            "date": pub_date,
            "summary": summary[:350],
            "content": content,
            "url": link,
        })

    return articles
