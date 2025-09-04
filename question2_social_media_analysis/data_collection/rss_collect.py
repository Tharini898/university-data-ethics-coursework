import os, argparse, csv, time
import feedparser

def collect_rss(feeds, out_csv):
    rows = []
    for url in feeds:
        print("Reading feed:", url)
        d = feedparser.parse(url)
        for e in d.entries:
            rows.append({
                "feed": url,
                "title": getattr(e, "title", ""),
                "summary": getattr(e, "summary", ""),
                "published": getattr(e, "published", ""),
                "link": getattr(e, "link", ""),
            })
        time.sleep(0.5)
    os.makedirs(os.path.dirname(out_csv) or ".", exist_ok=True)
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys() if rows else ["feed","title","summary","published","link"])
        writer.writeheader()
        writer.writerows(rows)
    print("Saved", len(rows), "RSS items to", out_csv)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--feeds", nargs="+", default=[
        "https://news.ycombinator.com/rss",
        "https://www.reddit.com/r/books/.rss"
    ])
    ap.add_argument("--out", default="data/rss/rss_items.csv")
    args = ap.parse_args()
    collect_rss(args.feeds, args.out)
