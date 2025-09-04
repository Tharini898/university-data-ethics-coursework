import os, time, csv, argparse, sys
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

BASE = "http://books.toscrape.com/"

def fetch(url, session, retries=3, backoff=1.5):
    for attempt in range(retries):
        try:
            resp = session.get(url, timeout=15)
            resp.raise_for_status()
            return resp
        except Exception as e:
            if attempt == retries - 1:
                raise
            time.sleep(backoff * (attempt + 1))

def parse_book(card, base_url):
    title = card.h3.a["title"].strip()
    rel_url = card.h3.a["href"]
    price = card.select_one(".price_color").text.strip().replace("£","")
    stock = card.select_one(".availability").text.strip()
    rating = card.select_one(".star-rating")["class"]
    rating_value = next((r for r in rating if r != "star-rating"), "Zero")
    detail_url = urljoin(base_url, rel_url)
    return {
        "title": title,
        "price": price,
        "stock": stock,
        "rating": rating_value,
        "url": detail_url
    }

def scrape_books(outdir):
    os.makedirs(outdir, exist_ok=True)
    session = requests.Session()
    url = BASE
    rows = []
    page_num = 1
    while True:
        print(f"Scraping page {page_num}: {url}")
        resp = fetch(url, session)
        soup = BeautifulSoup(resp.text, "lxml")
        for card in soup.select(".product_pod"):
            rows.append(parse_book(card, url))
        next_link = soup.select_one("li.next > a")
        if not next_link:
            break
        url = urljoin(url, next_link["href"])
        page_num += 1
        time.sleep(1.0)  # be nice
    # Save CSV & JSON
    csv_path = os.path.join(outdir, "books.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    import json
    with open(os.path.join(outdir, "books.json"), "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(rows)} records to {csv_path}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="data/books", help="Output directory")
    args = ap.parse_args()
    try:
        scrape_books(args.out)
    except Exception as e:
        print("ERROR:", e, file=sys.stderr)
        sys.exit(1)
