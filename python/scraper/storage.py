import csv
import os

FILE_NAME = "defence_news.csv"


def load_existing_urls():
    if not os.path.exists(FILE_NAME):
        return set()

    with open(FILE_NAME, newline="", encoding="utf-8") as f:
        return {row["url"] for row in csv.DictReader(f)}


def save_to_csv(articles):
    file_exists = os.path.isfile(FILE_NAME)
    existing_urls = load_existing_urls()

    with open(FILE_NAME, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "source",
                "category",
                "title",
                "date",
                "summary",
                "content",
                "url",
            ],
        )

        if not file_exists:
            writer.writeheader()

        for a in articles:
            if a["url"] not in existing_urls:
                writer.writerow(a)
