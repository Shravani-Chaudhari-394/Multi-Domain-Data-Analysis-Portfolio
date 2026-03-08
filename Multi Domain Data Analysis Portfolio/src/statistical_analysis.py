"""
statistical_analysis.py
-----------------------
Reusable statistical tests and summary functions for the Students Performance
dataset.  All functions return structured dictionaries so results can easily
be serialised to JSON or embedded in reports.
"""

import pandas as pd
import numpy as np
from scipy import stats
from itertools import combinations
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from data_loader import SCORE_COLUMNS


# ── Descriptive statistics ───────────────────────────────────────────────────

def descriptive_stats(df: pd.DataFrame, cols: list[str] | None = None) -> pd.DataFrame:
    """
    Return a tidy descriptive-statistics table for numeric columns.

    Parameters
    ----------
    df   : pd.DataFrame
    cols : list of column names (default: SCORE_COLUMNS + average_score)

    Returns
    -------
    pd.DataFrame  – mean, median, std, skew, kurtosis, min, max, IQR
    """
    if cols is None:
        cols = SCORE_COLUMNS + ["average_score"]

    rows = []
    for col in cols:
        s = df[col].dropna()
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        rows.append({
            "column":   col,
            "mean":     round(s.mean(), 2),
            "median":   round(s.median(), 2),
            "std":      round(s.std(), 2),
            "skewness": round(s.skew(), 3),
            "kurtosis": round(s.kurt(), 3),
            "min":      s.min(),
            "max":      s.max(),
            "iqr":      round(q3 - q1, 2),
        })
    return pd.DataFrame(rows).set_index("column")


# ── Normality ────────────────────────────────────────────────────────────────

def normality_tests(df: pd.DataFrame, cols: list[str] | None = None) -> pd.DataFrame:
    """
    Run Shapiro-Wilk normality test on each numeric column.

    Returns
    -------
    pd.DataFrame  – statistic, p_value, is_normal (α=0.05)
    """
    if cols is None:
        cols = SCORE_COLUMNS + ["average_score"]

    rows = []
    for col in cols:
        sample = df[col].dropna()
        # Shapiro-Wilk is reliable for n < 5000; subsample if larger
        if len(sample) > 5000:
            sample = sample.sample(5000, random_state=42)
        stat, p = stats.shapiro(sample)
        rows.append({
            "column":    col,
            "W_stat":    round(stat, 4),
            "p_value":   round(p, 4),
            "is_normal": p >= 0.05,
        })
    return pd.DataFrame(rows).set_index("column")


# ── Group comparisons ────────────────────────────────────────────────────────

def t_test_two_groups(
    df: pd.DataFrame,
    group_col: str,
    value_col: str,
    alpha: float = 0.05,
) -> dict:
    """
    Independent-samples t-test between two groups.

    Parameters
    ----------
    df        : pd.DataFrame
    group_col : column that defines the two groups (must have exactly 2 unique values)
    value_col : numeric column to compare
    alpha     : significance level

    Returns
    -------
    dict with keys: groups, means, t_stat, p_value, significant, effect_size (Cohen's d)
    """
    groups = df[group_col].dropna().unique()
    if len(groups) != 2:
        raise ValueError(f"Expected 2 groups in '{group_col}', found {len(groups)}: {groups}")

    a = df[df[group_col] == groups[0]][value_col].dropna()
    b = df[df[group_col] == groups[1]][value_col].dropna()

    t_stat, p_val = stats.ttest_ind(a, b, equal_var=False)  # Welch's t-test

    # Cohen's d
    pooled_std = np.sqrt((a.std() ** 2 + b.std() ** 2) / 2)
    cohen_d = (a.mean() - b.mean()) / pooled_std if pooled_std else 0

    return {
        "groups":      {str(groups[0]): round(a.mean(), 2), str(groups[1]): round(b.mean(), 2)},
        "t_stat":      round(t_stat, 4),
        "p_value":     round(p_val, 4),
        "significant": p_val < alpha,
        "cohen_d":     round(cohen_d, 4),
        "effect_size": _cohen_d_label(abs(cohen_d)),
    }


def _cohen_d_label(d: float) -> str:
    if d < 0.2:  return "negligible"
    if d < 0.5:  return "small"
    if d < 0.8:  return "medium"
    return "large"


def anova_test(
    df: pd.DataFrame,
    group_col: str,
    value_col: str,
    alpha: float = 0.05,
) -> dict:
    """
    One-way ANOVA across multiple groups, followed by Tukey HSD post-hoc.

    Returns
    -------
    dict with f_stat, p_value, significant, group_means, tukey_results
    """
    from statsmodels.stats.multicomp import pairwise_tukeyhsd

    groups = df[group_col].dropna().unique()
    samples = [df[df[group_col] == g][value_col].dropna() for g in groups]
    f_stat, p_val = stats.f_oneway(*samples)

    tukey = pairwise_tukeyhsd(
        endog=df[value_col].dropna(),
        groups=df.loc[df[value_col].notna(), group_col],
        alpha=alpha,
    )

    return {
        "group_col":   group_col,
        "value_col":   value_col,
        "f_stat":      round(f_stat, 4),
        "p_value":     round(p_val, 6),
        "significant": p_val < alpha,
        "group_means": {
            str(g): round(s.mean(), 2) for g, s in zip(groups, samples)
        },
        "tukey_summary": str(tukey),
    }


def chi_square_test(
    df: pd.DataFrame,
    col1: str,
    col2: str,
    alpha: float = 0.05,
) -> dict:
    """
    Chi-square test of independence between two categorical columns.

    Returns
    -------
    dict with chi2, p_value, dof, significant, cramers_v
    """
    ct = pd.crosstab(df[col1], df[col2])
    chi2, p_val, dof, _ = stats.chi2_contingency(ct)

    # Cramér's V
    n = ct.values.sum()
    cramers_v = np.sqrt(chi2 / (n * (min(ct.shape) - 1)))

    return {
        "col1":        col1,
        "col2":        col2,
        "chi2":        round(chi2, 4),
        "p_value":     round(p_val, 6),
        "dof":         dof,
        "significant": p_val < alpha,
        "cramers_v":   round(cramers_v, 4),
        "association": _cramers_v_label(cramers_v),
    }


def _cramers_v_label(v: float) -> str:
    if v < 0.1:  return "negligible"
    if v < 0.3:  return "small"
    if v < 0.5:  return "medium"
    return "large"


# ── Correlation ──────────────────────────────────────────────────────────────

def correlation_analysis(
    df: pd.DataFrame,
    cols: list[str] | None = None,
    method: str = "pearson",
) -> pd.DataFrame:
    """
    Pairwise correlation matrix for numeric columns.

    Parameters
    ----------
    method : 'pearson' | 'spearman' | 'kendall'
    """
    if cols is None:
        cols = SCORE_COLUMNS + ["average_score"]
    return df[cols].corr(method=method).round(3)


# ── Pass-rate helpers ────────────────────────────────────────────────────────

def pass_rate_by_group(
    df: pd.DataFrame,
    group_col: str,
    threshold: int = 60,
) -> pd.DataFrame:
    """
    Compute pass rate (avg_score ≥ threshold) for each category in group_col.
    """
    result = (
        df.groupby(group_col)
        .apply(lambda x: (x["average_score"] >= threshold).mean() * 100)
        .reset_index(name="pass_rate_%")
    )
    result["pass_rate_%"] = result["pass_rate_%"].round(2)
    return result.sort_values("pass_rate_%", ascending=False)


# ── Summary table ────────────────────────────────────────────────────────────

def full_stats_report(df: pd.DataFrame) -> dict:
    """
    Run the complete statistical battery and return results as a nested dict.
    Intended to be consumed by report_generator.py.
    """
    report = {}

    print("📐 Descriptive statistics …")
    report["descriptive"] = descriptive_stats(df).to_dict()

    print("📐 Normality tests …")
    report["normality"] = normality_tests(df).to_dict()

    print("📐 Gender vs average score (t-test) …")
    report["gender_t_test"] = t_test_two_groups(df, "gender", "average_score")

    print("📐 Test-prep vs average score (t-test) …")
    report["testprep_t_test"] = t_test_two_groups(df, "test preparation course", "average_score")

    print("📐 Lunch vs average score (t-test) …")
    report["lunch_t_test"] = t_test_two_groups(df, "lunch", "average_score")

    print("📐 Parental education vs average score (ANOVA) …")
    report["edu_anova"] = anova_test(df, "parental level of education", "average_score")

    print("📐 Ethnic group vs average score (ANOVA) …")
    report["ethnicity_anova"] = anova_test(df, "race/ethnicity", "average_score")

    print("📐 Correlation matrix …")
    report["correlation"] = correlation_analysis(df).to_dict()

    print("📐 Pass rates by gender …")
    report["pass_rate_gender"] = pass_rate_by_group(df, "gender").to_dict()

    print("📐 Pass rates by test prep …")
    report["pass_rate_testprep"] = pass_rate_by_group(df, "test preparation course").to_dict()

    print("✅ Statistical analysis complete.\n")
    return report
