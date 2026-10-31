# Netflix Insights — Power BI Dashboard

An interactive data analysis project exploring 5,283 Netflix movie and TV show titles, IMDb ratings, and audience voting activity using Python and Power BI.

## Dashboard Features

- Total titles and average IMDb score KPIs
- Interactive content-type slicer
- Release-era slicer
- IMDb rating by viewing category
- IMDb ratings versus vote count scatter chart
- Netflix-inspired dark theme
- Reset filters button

## Python Exploratory Data Analysis (EDA)

Extended the project using Python to perform exploratory data analysis on the Netflix dataset.

### Analysis Performed

- Dataset profiling, missing-value analysis and duplicate detection.
- Compared average and median IMDb ratings across Movies and TV Shows.
- Analyzed content distribution across release years.
- Compared IMDb vote counts across content types.
- Examined the relationship between IMDb ratings and vote counts using Pearson and Spearman correlation.
- Grouped titles into five release-era categories.

### Key Findings

- Analyzed 5,283 titles, including 3,407 Movies and 1,876 TV Shows.
- TV Shows recorded an average IMDb score of 7.02/10 compared to 6.27/10 for Movies.
- Identified missing values in descriptions, age certifications and IMDb votes.
- Found zero duplicate records.

### Python Outputs

Generated visualizations and statistical summaries are available in the `python/outputs/` directory.

## Tools & Technologies

- Python (Pandas, Matplotlib)
- Power BI Desktop
- DAX
- Power Query
- Excel 365
- Git and GitHub

## Business Questions

1. How do IMDb scores vary across viewing categories?
2. How do IMDb ratings relate to IMDb vote counts?
3. How can the catalog be explored by release era and content type?
4. How does content distribution vary between Movies and TV Shows across release years?

## Data Note

IMDb votes indicate voting activity on IMDb, not Netflix viewing hours.

## Files

- `Netflix_Visuals.pbix` — Power BI report
- `3D Red Netflix N Logo.png` — Dashboard logo
- `Netflix TV Shows and Movies.xlsx` — Source dataset, if redistribution is permitted
- `python/netflix_eda.py` — Python EDA script
- `python/requirements.txt` — Python dependencies
- `python/outputs/` — Generated charts and analysis reports

## How to Run Python Analysis

Install the required libraries:

```bash
pip install -r python/requirements.txt
```

Run the analysis:

```bash
python python/netflix_eda.py
```

Generated outputs will be saved in `python/outputs/`.

## How to View the Dashboard

Download the PBIX file and open it in Power BI Desktop.