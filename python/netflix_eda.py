"""
Netflix Content Analysis - Python EDA add-on
Reads the existing Excel source file. It does not modify the workbook or PBIX.
Run from any working directory:
    python python/netflix_eda.py
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_DIR = Path(__file__).resolve().parent.parent
SOURCE_FILE = PROJECT_DIR / "Netflix TV Shows and Movies.xlsx"
OUTPUT_DIR = PROJECT_DIR / "python" / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

plt.style.use("default")

# 1) Load the existing source workbook
df = pd.read_excel(SOURCE_FILE, sheet_name=0)

# Standardize the content-type labels for readable reporting.
df["type"] = df["type"].astype(str).str.strip().str.upper()
df["imdb_score"] = pd.to_numeric(df["imdb_score"], errors="coerce")
df["imdb_votes"] = pd.to_numeric(df["imdb_votes"], errors="coerce")
df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce")

print("=" * 60)
print("NETFLIX CONTENT ANALYSIS - PYTHON EDA")
print("=" * 60)
print(f"Dataset shape: {df.shape[0]:,} rows x {df.shape[1]} columns")
print("\nContent type counts:")
print(df["type"].value_counts())
print("\nMissing values:")
print(df.isna().sum())
print(f"\nDuplicate rows: {df.duplicated().sum():,}")

# 2) Content-type overview: title count, mean score and mean votes
type_summary = (
    df.groupby("type", dropna=False)
      .agg(
          title_count=("id", "count"),
          average_imdb_score=("imdb_score", "mean"),
          median_imdb_score=("imdb_score", "median"),
          average_imdb_votes=("imdb_votes", "mean"),
          median_imdb_votes=("imdb_votes", "median"),
      )
      .reset_index()
)
type_summary.to_csv(OUTPUT_DIR / "content_type_summary.csv", index=False)
print("\nContent type summary:")
print(type_summary.round(2).to_string(index=False))

# 3) Average IMDb score by content type
plt.figure(figsize=(8, 5))
plt.bar(type_summary["type"], type_summary["average_imdb_score"])
plt.title("Average IMDb Score by Content Type")
plt.xlabel("Content Type")
plt.ylabel("Average IMDb Score (out of 10)")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "average_rating_by_type.png", dpi=180)
plt.close()

# 4) Catalog release-year trend, split by content type
yearly = (
    df.dropna(subset=["release_year"])
      .groupby(["release_year", "type"])
      .size()
      .reset_index(name="title_count")
)
yearly.to_csv(OUTPUT_DIR / "release_year_content_counts.csv", index=False)

plt.figure(figsize=(11, 5))
for content_type, group in yearly.groupby("type"):
    plt.plot(group["release_year"], group["title_count"], marker="o", label=content_type)
plt.legend()
plt.title("Netflix Titles by Release Year and Content Type")
plt.xlabel("Release Year")
plt.ylabel("Number of Titles")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "release_year_trend.png", dpi=180)
plt.close()

# 5) IMDb vote activity: median is included because vote counts are skewed.
votes = df.dropna(subset=["imdb_votes"]).copy()
plt.figure(figsize=(8, 5))
box_data = [votes.loc[votes["type"] == content_type, "imdb_votes"].dropna()
            for content_type in sorted(votes["type"].dropna().unique())]
plt.boxplot(box_data, labels=sorted(votes["type"].dropna().unique()))
plt.yscale("log")
plt.title("IMDb Vote Counts by Content Type (Log Scale)")
plt.xlabel("Content Type")
plt.ylabel("IMDb Votes (log scale)")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "vote_count_by_type.png", dpi=180)
plt.close()

# 6) Relationship between score and votes.
score_votes = df.dropna(subset=["imdb_score", "imdb_votes"])
pearson = score_votes["imdb_score"].corr(score_votes["imdb_votes"], method="pearson")
spearman = score_votes["imdb_score"].corr(score_votes["imdb_votes"], method="spearman")
correlation_summary = pd.DataFrame({
    "measure": ["Pearson correlation", "Spearman correlation"],
    "value": [pearson, spearman],
    "records_used": [len(score_votes), len(score_votes)]
})
correlation_summary.to_csv(OUTPUT_DIR / "rating_vote_correlation.csv", index=False)

plt.figure(figsize=(8, 5))
for content_type, group in score_votes.groupby("type"):
    plt.scatter(group["imdb_votes"], group["imdb_score"], alpha=0.45, s=18, label=content_type)
plt.legend()
plt.xscale("log")
plt.title("IMDb Score vs IMDb Vote Count")
plt.xlabel("IMDb Votes (log scale)")
plt.ylabel("IMDb Score")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "score_vs_votes.png", dpi=180)
plt.close()

# 7) Release-era summary (5 broad eras) for a compact catalog view.
bins = [1950, 1980, 2000, 2010, 2015, 2023]
labels = ["1951-1980", "1981-2000", "2001-2010", "2011-2015", "2016-2022"]
df["release_era_python"] = pd.cut(
    df["release_year"], bins=bins, labels=labels, include_lowest=True
)
era_summary = (
    df.groupby(["release_era_python", "type"], observed=False)
      .size()
      .reset_index(name="title_count")
)
era_summary.to_csv(OUTPUT_DIR / "release_era_summary.csv", index=False)

# 8) A concise text report with dataset-specific outputs.
report = [
    "NETFLIX CONTENT ANALYSIS - PYTHON SUMMARY",
    f"Rows analyzed: {len(df):,}",
    f"Columns: {len(df.columns) - 1:,} original columns plus release_era_python",
    f"Duplicate rows: {df.duplicated().sum():,}",
    "",
    "Average IMDb score by content type:",
    type_summary[["type", "title_count", "average_imdb_score"]].round(2).to_string(index=False),
    "",
    f"Pearson correlation (IMDb score vs votes): {pearson:.3f}",
    f"Spearman correlation (IMDb score vs votes): {spearman:.3f}",
    "",
    "Note: IMDb votes represent IMDb voting activity, not Netflix viewing hours.",
]
(OUTPUT_DIR / "analysis_summary.txt").write_text("\n".join(report), encoding="utf-8")

print(f"\nAnalysis complete. Outputs saved to: {OUTPUT_DIR}")
