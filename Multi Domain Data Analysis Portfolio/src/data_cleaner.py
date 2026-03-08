"""
data_cleaner.py
---------------
Reusable functions for cleaning and feature-engineering the Students
Performance dataset.
"""

import pandas as pd
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from data_loader import SCORE_COLUMNS, CATEGORICAL_COLUMNS


# ── Education level ordering (low → high) ──────────────────────────────────
EDUCATION_ORDER = [
    "some high school",
    "high school",
    "some college",
    "associate's degree",
    "bachelor's degree",
    "master's degree",
]


def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove exact duplicate rows and report how many were dropped."""
    before = len(df)
    df = df.drop_duplicates()
    dropped = before - len(df)
    if dropped:
        print(f"⚠️  Dropped {dropped} duplicate row(s).")
    else:
        print("✅ No duplicate rows found.")
    return df


def handle_missing_values(
    df: pd.DataFrame,
    numeric_strategy: str = "median",
    categorical_strategy: str = "mode",
) -> pd.DataFrame:
    """
    Impute missing values.

    Parameters
    ----------
    df : pd.DataFrame
    numeric_strategy : 'mean' | 'median' | 'drop'
    categorical_strategy : 'mode' | 'unknown' | 'drop'

    Returns
    -------
    pd.DataFrame
    """
    df = df.copy()

    # Numeric columns
    num_missing = df[SCORE_COLUMNS].isnull().sum().sum()
    if num_missing:
        if numeric_strategy == "drop":
            df = df.dropna(subset=SCORE_COLUMNS)
        elif numeric_strategy == "mean":
            df[SCORE_COLUMNS] = df[SCORE_COLUMNS].fillna(df[SCORE_COLUMNS].mean())
        else:  # median
            df[SCORE_COLUMNS] = df[SCORE_COLUMNS].fillna(df[SCORE_COLUMNS].median())
        print(f"✅ Imputed {num_missing} numeric missing value(s) using '{numeric_strategy}'.")
    else:
        print("✅ No missing numeric values.")

    # Categorical columns
    cat_missing = df[CATEGORICAL_COLUMNS].isnull().sum().sum()
    if cat_missing:
        if categorical_strategy == "drop":
            df = df.dropna(subset=CATEGORICAL_COLUMNS)
        elif categorical_strategy == "unknown":
            df[CATEGORICAL_COLUMNS] = df[CATEGORICAL_COLUMNS].fillna("Unknown")
        else:  # mode
            for col in CATEGORICAL_COLUMNS:
                if df[col].isnull().any():
                    df[col] = df[col].fillna(df[col].mode()[0])
        print(f"✅ Imputed {cat_missing} categorical missing value(s) using '{categorical_strategy}'.")
    else:
        print("✅ No missing categorical values.")

    return df


def encode_education_ordinal(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add an ordinal integer column for 'parental level of education'
    (0 = lowest, 5 = highest).
    """
    df = df.copy()
    edu_map = {level: i for i, level in enumerate(EDUCATION_ORDER)}
    df["education_level_num"] = (
        df["parental level of education"].str.lower().map(edu_map)
    )
    return df


def add_derived_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Engineer additional columns that support the analysis:
      - average_score  : mean of the three test scores
      - total_score    : sum of the three test scores
      - score_std      : std across the three scores per student (consistency)
      - passed_all     : True if all three scores >= 60
      - grade          : letter grade based on average_score
    """
    df = df.copy()
    df["average_score"] = df[SCORE_COLUMNS].mean(axis=1).round(2)
    df["total_score"] = df[SCORE_COLUMNS].sum(axis=1)
    df["score_std"] = df[SCORE_COLUMNS].std(axis=1).round(2)
    df["passed_all"] = (df[SCORE_COLUMNS] >= 60).all(axis=1)

    bins = [0, 59, 69, 79, 89, 100]
    labels = ["F", "D", "C", "B", "A"]
    df["grade"] = pd.cut(
        df["average_score"], bins=bins, labels=labels, right=True, include_lowest=True
    )
    return df


def standardize_categoricals(df: pd.DataFrame) -> pd.DataFrame:
    """Lowercase and strip whitespace from all categorical columns."""
    df = df.copy()
    for col in CATEGORICAL_COLUMNS:
        df[col] = df[col].str.strip().str.lower()
    return df


def clean_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """
    Full cleaning pipeline:
      1. Drop duplicates
      2. Standardize categorical text
      3. Handle missing values
      4. Encode education ordinal
      5. Add derived features

    Parameters
    ----------
    df : pd.DataFrame  – raw data from load_data()

    Returns
    -------
    pd.DataFrame  – cleaned, feature-enriched data
    """
    print("\n🔧 Running cleaning pipeline …")
    df = drop_duplicates(df)
    df = standardize_categoricals(df)
    df = handle_missing_values(df)
    df = encode_education_ordinal(df)
    df = add_derived_features(df)
    print(f"✅ Pipeline complete. Final shape: {df.shape}\n")
    return df
