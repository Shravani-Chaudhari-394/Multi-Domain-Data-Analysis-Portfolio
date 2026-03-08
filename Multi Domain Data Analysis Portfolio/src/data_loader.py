"""
data_loader.py
--------------
Reusable functions for loading and validating the Students Performance dataset.
"""

import pandas as pd
import os
from pathlib import Path


EXPECTED_COLUMNS = [
    "gender",
    "race/ethnicity",
    "parental level of education",
    "lunch",
    "test preparation course",
    "math score",
    "reading score",
    "writing score",
]

SCORE_COLUMNS = ["math score", "reading score", "writing score"]
CATEGORICAL_COLUMNS = [
    "gender",
    "race/ethnicity",
    "parental level of education",
    "lunch",
    "test preparation course",
]


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load the Students Performance CSV file into a DataFrame.

    Parameters
    ----------
    filepath : str
        Path to the CSV file.

    Returns
    -------
    pd.DataFrame
        Raw loaded DataFrame.

    Raises
    ------
    FileNotFoundError
        If the file does not exist at the given path.
    ValueError
        If required columns are missing.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    df = pd.read_csv(filepath)

    # Validate columns
    missing = [c for c in EXPECTED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing expected columns: {missing}")

    print(f"✅ Data loaded successfully: {df.shape[0]} rows × {df.shape[1]} columns")
    return df


def get_data_summary(df: pd.DataFrame) -> dict:
    """
    Return a structured summary dictionary for the loaded DataFrame.

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    dict
        Summary with shape, dtypes, missing values, and basic stats.
    """
    summary = {
        "shape": df.shape,
        "dtypes": df.dtypes.to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "missing_pct": (df.isnull().mean() * 100).round(2).to_dict(),
        "numeric_stats": df[SCORE_COLUMNS].describe().to_dict(),
        "categorical_counts": {
            col: df[col].value_counts().to_dict() for col in CATEGORICAL_COLUMNS
        },
    }
    return summary


def print_data_summary(df: pd.DataFrame) -> None:
    """Pretty-print the dataset summary to console."""
    summary = get_data_summary(df)
    print("\n" + "=" * 60)
    print("📊 DATASET SUMMARY")
    print("=" * 60)
    print(f"  Rows    : {summary['shape'][0]}")
    print(f"  Columns : {summary['shape'][1]}")

    print("\n📌 Missing Values:")
    for col, cnt in summary["missing_values"].items():
        flag = "⚠️ " if cnt > 0 else "✅"
        print(f"  {flag} {col}: {cnt} ({summary['missing_pct'][col]}%)")

    print("\n📌 Score Statistics:")
    for col in SCORE_COLUMNS:
        stats = summary["numeric_stats"][col]
        print(
            f"  {col:15s} → mean={stats['mean']:.1f}, "
            f"std={stats['std']:.1f}, "
            f"min={stats['min']:.0f}, max={stats['max']:.0f}"
        )
    print("=" * 60)
