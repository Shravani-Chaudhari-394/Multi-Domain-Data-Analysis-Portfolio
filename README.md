# 📊 Data Analysis Portfolio

A collection of **5 end-to-end data analysis projects** built with Python and Jupyter,
covering sales, education, weather, finance, and social media domains.
Each project follows the same folder structure, shared `src/` modules, and
consistent storytelling approach — every chart answers a specific business question.

---

## 🗂️ Project Structure

```
project_root/
│
├── data/                          ← All CSV datasets
│   ├── supermarket_sales.csv      (Project 1)
│   ├── StudentsPerformance.csv    (Project 2)
│   ├── climate_data.csv           (Project 3)
│   ├── INDIAVIX.csv               (Project 4)
│   └── sentimentdataset.csv       (Project 5)
│
├── notebooks/                     ← One notebook per project
│   ├── project1_sales_analysis.ipynb
│   ├── project2_student_performance_analysis.ipynb
│   ├── project3_weather_analysis.ipynb
│   ├── project4_finance_vix_analysis.ipynb
│   └── project5_social_media_analytics.ipynb
│
├── src/                           ← Shared reusable modules
│   ├── path_config.py             ← Auto path resolver (used by ALL notebooks)
│   ├── data_loader.py             ← Generic CSV loading & validation
│   ├── data_cleaner.py            ← Cleaning pipeline & feature engineering
│   ├── visualization.py           ← Reusable chart templates
│   ├── statistical_analysis.py    ← Hypothesis tests, correlation, ANOVA
│   └── report_generator.py        ← Markdown & JSON report export
│
├── outputs/                       ← Auto-created on first run
│   ├── project1/figures/
│   ├── project2/figures/
│   ├── project3/figures/
│   ├── project4/figures/
│   └── project5/figures/
│
├── requirements.txt
└── README.md
```

---

## ⚡ Quick Start

```bash
# 1. Clone or download this repository
# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Mac / Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch JupyterLab
jupyter lab

# 5. Open any notebook from notebooks/ and Run All
```

> **Note:** All notebooks auto-detect `src/` and `data/` using `path_config.py`.
> No manual path edits required as long as the folder structure above is maintained.

---

## 📁 Projects

### 🛒 Project 1 — Supermarket Sales Analysis
`notebooks/project1_sales_analysis.ipynb`

**Dataset:** `supermarket_sales.csv` — 2,000 transactions across 3 branches (Jan–Dec 2023)

**Goal:** Analyse daily sales patterns, identify best-selling products, and understand customer behaviour.

| # | Business Question |
|---|-------------------|
| Q1  | Overall KPIs — revenue, volume, basket size |
| Q2  | Which product lines generate the most revenue and highest ratings? |
| Q3  | How do daily and monthly sales trend across the year? |
| Q4  | What are the peak shopping hours and busiest days? |
| Q5  | How does each branch compare on revenue, ratings, and product mix? |
| Q6  | Member vs Normal customer differences |
| Q7  | Gender influence on product preferences and spending |
| Q8  | Payment method preferences and spend impact |
| Q9  | What drives customer satisfaction ratings? |
| Q10 | Highest-value customer segments (RFM-style) |

**Key techniques:** Time-series trend analysis · RFM segmentation · Dual-axis charts ·
Day×Hour heatmaps · Mann-Whitney U · Kruskal-Wallis · Pearson correlation

---

### 🎓 Project 2 — Student Performance Analysis
`notebooks/project2_student_performance_analysis.ipynb`

**Dataset:** `StudentsPerformance.csv` — 1,000 student exam records

**Goal:** Understand what factors (parental education, test prep, lunch type, gender)
drive academic performance across math, reading, and writing.

| # | Business Question |
|---|-------------------|
| Q1  | How are student scores distributed across subjects? |
| Q2  | Does gender influence academic performance? |
| Q3  | Does completing a test-prep course improve scores? |
| Q4  | How does parental education level affect scores? |
| Q5  | Does lunch type signal socioeconomic impact? |
| Q6  | How do scores vary across ethnic groups? |
| Q7  | How strongly are math, reading, and writing correlated? |
| Q8  | What share of students achieve each letter grade? |
| Q9  | What combination of factors predicts high performance? |

**Key techniques:** One-way ANOVA · Tukey HSD post-hoc · t-tests · Cohen's d ·
Cramér's V · Correlation matrix · Grade distribution analysis

---

### 🌦️ Project 3 — Weather Data Analysis
`notebooks/project3_weather_analysis.ipynb`

**Dataset:** `climate_data.csv` — 3,902 daily weather records (2009–2020)

**Goal:** Analyse temperature trends, seasonal patterns, rainfall distribution,
and extreme weather events over a 12-year period.

| # | Business Question |
|---|-------------------|
| Q1  | How has average temperature trended over the years? |
| Q2  | What are the seasonal temperature patterns across months? |
| Q3  | How is daily rainfall distributed — when does it peak? |
| Q4  | Which months and seasons receive the most rainfall? |
| Q5  | How do humidity and dewpoint vary across seasons? |
| Q6  | Relationship between temperature, humidity, and heat index |
| Q7  | When do extreme heat and cold events occur? |
| Q8  | How do wind speed and gust speed vary by season? |
| Q9  | What does pressure differential signal about weather volatility? |
| Q10 | Are summers getting hotter and winters milder YoY? |

**Key techniques:** Linear regression trend lines · Bollinger-style rolling windows ·
Extreme event calendar heatmaps · Seasonal decomposition · Pearson correlation

---

### 📈 Project 4 — India VIX Finance Analysis
`notebooks/project4_finance_vix_analysis.ipynb`

**Dataset:** `INDIAVIX.csv` — 2,769 daily VIX records (2009–2020)

**Goal:** Analyse the India VIX fear index — trend structure, regime detection,
spike clustering, mean-reversion speed, and year-over-year volatility shifts.

| # | Business Question |
|---|-------------------|
| Q1  | How has India VIX trended over 2009–2020? Major fear spikes? |
| Q2  | What does the daily return distribution of VIX look like? |
| Q3  | How volatile is VIX itself? (Volatility-of-Volatility) |
| Q4  | What are the seasonal / monthly patterns in VIX? |
| Q5  | Can we identify distinct VIX market regimes? |
| Q6  | How large are daily VIX swings (High–Low range)? |
| Q7  | What do rolling MA signals say about market cycles? |
| Q8  | Are VIX spikes clustered? How long do fear episodes last? |
| Q9  | Autocorrelation structure and mean-reversion analysis |
| Q10 | Is the market becoming more or less volatile YoY? |

**Key techniques:** Bollinger Bands · Z-score normalisation · Market regime classification ·
Volatility clustering (ACF) · OLS mean-reversion test · Ridgeline distribution plots ·
Crisis event annotation · Log-return fat-tail analysis

---

### 📱 Project 5 — Social Media Analytics
`notebooks/project5_social_media_analytics.ipynb`

**Dataset:** `sentimentdataset.csv` — 732 posts across Twitter, Instagram, Facebook (2010–2023)

**Goal:** Analyse sentiment patterns, platform engagement, geographic reach,
hashtag performance, and user behaviour across social platforms.

| # | Business Question |
|---|-------------------|
| Q1  | What is the overall sentiment landscape across all posts? |
| Q2  | How do sentiment patterns differ across platforms? |
| Q3  | Which emotions drive the highest engagement? |
| Q4  | How does posting activity and sentiment vary by hour and day? |
| Q5  | What are the geographic sentiment patterns by country? |
| Q6  | Which hashtags are most popular and what sentiment do they carry? |
| Q7  | How has sentiment trended year-over-year? |
| Q8  | Engagement distribution across platforms |
| Q9  | Are there power users? What is the user engagement footprint? |
| Q10 | What text patterns distinguish positive from negative posts? |

**Key techniques:** Sentiment polarity classification · Log-odds ratio word analysis ·
Lorenz engagement curve · Hashtag frequency vs engagement bubble chart ·
Mann-Whitney U · Kruskal-Wallis · Temporal heatmaps · Influencer scoring

---

## 🔧 Shared `src/` Modules

All notebooks import from a single shared `src/` package —
write once, reuse across every project.

| Module | Purpose |
|--------|---------|
| `path_config.py` | Auto-resolves `data/`, `src/`, and `outputs/` paths from any notebook location |
| `data_loader.py` | Generic CSV loading, column validation, summary printing |
| `data_cleaner.py` | Cleaning pipeline: deduplication, missing values, ordinal encoding, feature engineering |
| `visualization.py` | Reusable chart functions — each answers a named business question |
| `statistical_analysis.py` | t-tests, ANOVA, chi-square, Tukey HSD, correlation, pass-rate helpers |
| `report_generator.py` | Exports Markdown and JSON analysis reports to `outputs/` |

---

## 📦 Dependencies

```
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
scipy>=1.10.0
statsmodels>=0.14.0
jupyterlab>=4.0.0
notebook>=7.0.0
ipykernel>=6.0.0
```

Install: `pip install -r requirements.txt`

---

## 🎨 Design Principles

- **Story-first** — every visualisation answers a named business question
- **Consistent style** — shared colour palettes and formatting across all projects
- **Non-technical friendly** — each chart includes a plain-English insight callout
- **Reusable code** — all common operations live in `src/`, not duplicated in notebooks
- **Statistical rigour** — key findings backed by hypothesis tests with p-values reported
- **Executive-ready** — every project ends with a one-page dashboard and a recommendations section

