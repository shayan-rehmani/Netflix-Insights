# Python EDA Add-on

This folder adds Python exploratory data analysis to the existing Netflix Power BI project.
The original Excel workbook, PBIX dashboard, screenshots, and root README are left unchanged.

## Run

From the project root:

```bash
python -m pip install -r python/requirements.txt
python python/netflix_eda.py
```

The script reads `Netflix TV Shows and Movies.xlsx` from the project root and writes
charts, CSV summaries, and a text report into `python/outputs/`.

## Analyses

- Dataset profile, missing values, and duplicate-row check
- Movies vs TV Shows: title counts, average/median IMDb score, average/median IMDb votes
- Release-year catalog trend by content type
- IMDb vote-count comparison (log scale)
- IMDb score vs IMDb vote-count correlation (Pearson and Spearman)
- Five release-era content counts

IMDb votes are a measure of activity on IMDb, not Netflix viewing hours. The workbook
contains no genre column, so this add-on does not claim to perform genre analysis.
