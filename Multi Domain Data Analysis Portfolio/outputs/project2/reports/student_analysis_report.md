# 🎓 Student Performance Analysis Report

_Generated: 2026-03-06 23:58_



## Executive Summary

This report analyses academic performance data for **1000 students** across 14 variables including gender, parental education, test preparation, and lunch type.

- Overall average score: **67.8 / 100**
- Highest pass-rate group (by gender): **0** at 76.1%
- Test-preparation completion is associated with a **7.6-point** average score uplift


## Descriptive Statistics

| Metric | Mean | Std Dev | Skewness |
|--------|------|---------|----------|
| math score | 66.09 | 15.16 | -0.279 |
| reading score | 69.17 | 14.60 | -0.259 |
| writing score | 68.05 | 15.20 | -0.289 |
| average_score | 67.77 | 14.26 | -0.299 |


## Hypothesis Tests


### H1 · Gender and average score

  - Female: mean = 69.57
  - Male: mean = 65.84
  - ✅ Statistically significant (p = 0.0000)
  - Effect size (Cohen's d): 0.264 (small)

### H2 · Test-preparation course and average score

  - None: mean = 65.04
  - Completed: mean = 72.67
  - ✅ Statistically significant (p = 0.0000)
  - Effect size (Cohen's d): -0.560 (medium)

### H3 · Lunch type (socioeconomic proxy) and average score

  - Standard: mean = 70.84
  - Free/Reduced: mean = 62.20
  - ✅ Statistically significant (p = 0.0000)
  - Effect size (Cohen's d): 0.624 (medium)

### H4 · Parental education level and average score (ANOVA)

  - F-statistic: 10.7529
  - ✅ Statistically significant (p = 0.0000)
  - Highest-performing group: **master's degree** (mean = 73.60)

### H5 · Ethnic group and average score (ANOVA)

  - F-statistic: 9.0957
  - ✅ Statistically significant (p = 0.0000)


## Correlation Analysis

| | math score | reading score | writing score | average_score |
|---|---|---|---|---|
| **math score** | 1.000 | 0.818 | 0.803 | 0.919 |
| **reading score** | 0.818 | 1.000 | 0.955 | 0.970 |
| **writing score** | 0.803 | 0.955 | 1.000 | 0.966 |
| **average_score** | 0.919 | 0.970 | 0.966 | 1.000 |


## Key Findings & Recommendations

- **Test preparation matters**: Students who completed prep scored ~7.6 points higher on average.
- **Socioeconomic signals**: Lunch type is a significant predictor — consider targeted support programs for free/reduced lunch students.
- **Parental education gradient**: Higher parental education correlates with better student outcomes; family engagement programs may help.
- **Subject correlations are high** (r > 0.8): Strong readers tend to be strong writers — interdisciplinary literacy programs could be efficient.
- **Ethnic group gaps exist**: Targeted interventions for lower-performing groups should be considered.


## Appendix


Full statistical test outputs are available in the accompanying Jupyter notebook.