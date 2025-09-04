# University System + E-commerce Data Analysis + AI Ethics (Starter Repo)

This is a **beginner-friendly, production-style scaffold** for your coursework. It includes:
- **Question 1:** Object-Oriented University Management System (Python)
- **Question 2:** Multi-source scraping + cleaning + analysis + visualization (Python)
- **Question 3:** AI Ethics in Healthcare report (Markdown template)
- **Technical Report:** You will export your report to PDF (e.g., from VS Code or any Markdown tool).

## Quick Start

```bash
# 1) Create & activate a virtual environment (Windows PowerShell examples)
python -m venv .venv
. .venv/Scripts/Activate.ps1

# 2) Install dependencies
pip install -r requirements.txt

# 3) Run Q1 OOP demo
python question1_university_system/main.py

# 4) Run the Books scraper (Q2 - data collection)
python question2_ecommerce_analysis/data_collection/books_scraper.py --out data/books

# 5) Clean & preprocess scraped data
python question2_ecommerce_analysis/data_processing/cleaning.py --input data/books/books.csv --out data/clean

# 6) Run analysis & stats
python question2_ecommerce_analysis/analysis/stats.py --input data/clean/books_clean.csv --out reports

# 7) Make visualizations
python question2_ecommerce_analysis/visualizations/plots.py --input data/clean/books_clean.csv --out reports/figures

# 8) Use the ethics template for Q3 (write your content in Markdown)
# Open question3_ethics_report/healthcare_ethics_report.md and fill sections.
# Export to PDF (e.g., "Markdown PDF" VS Code extension).

# 9) Initialize Git (commit little and often!)
git init
git add .
git commit -m "Initial scaffold for coursework Q1-Q3"
```

## Repo Layout

```
project/
├── question1_university_system/
│   ├── main.py
│   ├── person.py
│   ├── student.py
│   ├── faculty.py
│   └── department.py
├── question2_ecommerce_analysis/
│   ├── data_collection/
│   │   ├── books_scraper.py
│   │   └── rss_collect.py
│   ├── data_processing/
│   │   └── cleaning.py
│   ├── analysis/
│   │   └── stats.py
│   └── visualizations/
│       └── plots.py
├── question3_ethics_report/
│   └── healthcare_ethics_report.md
├── requirements.txt
└── README.md
```

> Tip: add frequent commits: `git add -A && git commit -m "Message"`

## Notes
- All Python files include docstrings and validation.
- Q2 uses **requests + BeautifulSoup + feedparser + pandas**.
- Visualizations include **matplotlib** and **Plotly** (interactive HTML).
