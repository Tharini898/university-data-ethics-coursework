import os, re, argparse
import pandas as pd
from dateutil import parser as dateparser

def normalize_text(s: str) -> str:
    if not isinstance(s, str):
        return s
    s = s.replace("\n", " ").strip()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[^\w\s\-\.\,£$%:/]", "", s)
    return s

def standardize_date(s: str):
    try:
        return dateparser.parse(s).isoformat()
    except Exception:
        return None

def main(input_csv, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    df = pd.read_csv(input_csv)
    # Basic cleaning
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].map(normalize_text)
    # Duplicates
    before = len(df)
    df = df.drop_duplicates()
    # Convert price to float (handle currency symbols if present)
    if "price" in df.columns:
        df["price"] = df["price"].astype(str).str.replace("£","", regex=False).str.replace("$","", regex=False)
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
    # Ratings to numeric (map words to numbers if needed)
    if "rating" in df.columns:
        rating_map = {"Zero":0, "One":1, "Two":2, "Three":3, "Four":4, "Five":5}
        df["rating_num"] = df["rating"].map(rating_map).fillna(pd.to_numeric(df["rating"], errors="coerce"))
    # Dates standardization if exist
    for col in df.columns:
        if "date" in col.lower() or col.lower() in {"published"}:
            df[col] = df[col].map(standardize_date)
    # Quality checks
    after = len(df)
    report = {
        "rows_before": before,
        "rows_after": after,
        "null_counts": df.isna().sum().to_dict()
    }
    report_path = os.path.join(out_dir, "cleaning_report.json")
    df_out = os.path.join(out_dir, "books_clean.csv")
    df.to_csv(df_out, index=False)
    import json
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print("Saved cleaned data to", df_out)
    print("Cleaning report ->", report_path)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Input CSV path")
    ap.add_argument("--out", default="data/clean", help="Output directory")
    args = ap.parse_args()
    main(args.input, args.out)
