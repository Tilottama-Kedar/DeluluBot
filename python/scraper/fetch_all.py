from scraper.Defence.dd_news import fetch_dd_defence
from scraper.Defence.idrw import fetch_idrw_defence
from scraper.Defence.mod import fetch_mod_defence
from scraper.Defence.hindu_defence import fetch_hindu_defence
from scraper.storage import save_to_csv
from datetime import datetime


def fetch_all_defence(max_per_source=5):
    all_articles = []

    try:
        all_articles.extend(fetch_dd_defence(max_per_source))
    except Exception as e:
        print("DD error:", e)

    try:
        all_articles.extend(fetch_idrw_defence(max_per_source))
    except Exception as e:
        print("IDRW error:", e)

    try:
        all_articles.extend(fetch_mod_defence(max_per_source))
    except Exception as e:
        print("MOD error:", e)

    try:
        all_articles.extend(fetch_hindu_defence(max_per_source))
    except Exception as e:
        print("Hindu error:", e)

    def parse_date(article):
        try:
            return datetime.strptime(article["date"], "%Y-%m-%d")
        except:
            return datetime.min

    all_articles.sort(key=parse_date, reverse=True)
    return all_articles


if __name__ == "__main__":
    print("RUNNING ALL DEFENCE FETCH")

    news = fetch_all_defence()
    save_to_csv(news)   # 👈 ONLY storage call

    print(f"Total Articles Saved: {len(news)}")

    if news:
        print(news[0])
