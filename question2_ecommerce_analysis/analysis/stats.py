import os, argparse, json
import numpy as np
import pandas as pd
from scipy import stats

def describe(df):
    desc = {
        "price": df["price"].describe().to_dict() if "price" in df else {},
        "rating": df["rating_num"].describe().to_dict() if "rating_num" in df else {},
    }
    return desc

def detect_outliers(series, method="iqr"):
    series = series.dropna()
    if series.empty:
        return []
    if method == "iqr":
        q1, q3 = np.percentile(series, [25, 75])
        iqr = q3 - q1
        low, high = q1 - 1.5*iqr, q3 + 1.5*iqr
        idx = series[(series < low) | (series > high)].index.tolist()
        return idx
    z = np.abs(stats.zscore(series))
    return series[z > 3].index.tolist()

def correlation(df):
    cols = [c for c in ["price", "rating_num"] if c in df]
    if len(cols) < 2:
        return {}
    corr = df[cols].corr().to_dict()
    return corr

def hypothesis_test(df):
    # Example: one-way ANOVA across rating groups vs price
    if not {"price", "rating_num"} <= set(df.columns):
        return {}
    groups = [g["price"].dropna().values for _, g in df.groupby("rating_num")]
    if len(groups) < 2:
        return {}
    stat, p = stats.f_oneway(*groups)
    return {"anova_f": float(stat), "p_value": float(p)}

def main(input_csv, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    df = pd.read_csv(input_csv)
    results = {
        "descriptive": describe(df),
        "outliers_price_idx": detect_outliers(df["price"]) if "price" in df else [],
        "correlations": correlation(df),
        "anova_price_by_rating": hypothesis_test(df),
        "category_popularity": df["rating_num"].value_counts(dropna=False).to_dict() if "rating_num" in df else {}
    }
    with open(os.path.join(out_dir, "analysis_summary.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("Saved analysis summary to", os.path.join(out_dir, "analysis_summary.json"))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", default="reports")
    args = ap.parse_args()
    main(args.input, args.out)
