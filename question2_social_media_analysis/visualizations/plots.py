import os, argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

def ensure_dir(d):
    os.makedirs(d, exist_ok=True)

def hist_box(df, outdir):
    ensure_dir(outdir)
    if "price" in df:
        # Histogram
        plt.figure()
        df["price"].dropna().plot(kind="hist", bins=30)
        plt.title("Price Distribution")
        plt.xlabel("Price")
        plt.ylabel("Frequency")
        plt.savefig(os.path.join(outdir, "price_hist.png"))
        plt.close()

        # Boxplot
        plt.figure()
        df["price"].dropna().plot(kind="box")
        plt.title("Price Boxplot")
        plt.savefig(os.path.join(outdir, "price_box.png"))
        plt.close()

def scatter_trend(df, outdir):
    if not {"price", "rating_num"} <= set(df.columns):
        return
    ensure_dir(outdir)
    # Matplotlib scatter
    plt.figure()
    plt.scatter(df["rating_num"], df["price"])
    plt.title("Rating vs Price")
    plt.xlabel("Rating")
    plt.ylabel("Price")
    # Trend line
    x = df["rating_num"].dropna().values
    y = df["price"].dropna().values[:len(x)]
    if len(x) > 1:
        coeffs = np.polyfit(x[:len(y)], y, 1)
        line_x = np.linspace(min(x), max(x), 100)
        line_y = coeffs[0]*line_x + coeffs[1]
        plt.plot(line_x, line_y)
    plt.savefig(os.path.join(outdir, "rating_vs_price_scatter.png"))
    plt.close()

    # Plotly interactive
    fig = px.scatter(df, x="rating_num", y="price", hover_data=["title"] if "title" in df else None, trendline="ols")
    fig.write_html(os.path.join(outdir, "rating_vs_price_interactive.html"))

def bars(df, outdir):
    ensure_dir(outdir)
    if "rating_num" in df:
        counts = df["rating_num"].value_counts().sort_index()
        plt.figure()
        counts.plot(kind="bar")
        plt.title("Category Popularity (by Rating as Proxy)")
        plt.xlabel("Rating")
        plt.ylabel("Count")
        plt.savefig(os.path.join(outdir, "category_popularity.png"))
        plt.close()

def main(input_csv, out_dir):
    ensure_dir(out_dir)
    df = pd.read_csv(input_csv)
    hist_box(df, out_dir)
    scatter_trend(df, out_dir)
    bars(df, out_dir)
    print("Figures saved to", out_dir)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", default="reports/figures")
    args = ap.parse_args()
    main(args.input, args.out)
