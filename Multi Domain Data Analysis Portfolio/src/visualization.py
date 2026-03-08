

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import pandas as pd
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from data_loader import SCORE_COLUMNS

# ── Global style ────────────────────────────────────────────────────────────
PALETTE = {
    "primary":   "#4C72B0",
    "secondary": "#DD8452",
    "accent":    "#55A868",
    "highlight": "#C44E52",
    "neutral":   "#8172B2",
    "bg":        "#F8F9FA",
    "grid":      "#E0E0E0",
}

GENDER_PALETTE  = {"female": "#E91E8C", "male": "#1565C0"}
GROUP_PALETTE   = sns.color_palette("Set2", 5)
GRADE_PALETTE   = {"A": "#2E7D32", "B": "#558B2F", "C": "#F9A825",
                   "D": "#E65100", "F": "#B71C1C"}

sns.set_theme(style="whitegrid", font_scale=1.1)
plt.rcParams.update({
    "figure.facecolor": PALETTE["bg"],
    "axes.facecolor":   PALETTE["bg"],
    "axes.grid":        True,
    "grid.color":       PALETTE["grid"],
    "grid.linestyle":   "--",
    "grid.alpha":       0.7,
})


# ── Helpers ──────────────────────────────────────────────────────────────────

def _save_or_show(fig: plt.Figure, filepath: str | None) -> plt.Figure:
    fig.tight_layout()
    if filepath:
        fig.savefig(filepath, dpi=150, bbox_inches="tight")
        print(f"  💾 Saved → {filepath}")
    return fig


def _add_value_labels(ax, fmt=".1f", fontsize=9):
    """Annotate bars with their values."""
    for p in ax.patches:
        h = p.get_height()
        if np.isnan(h) or h == 0:
            continue
        ax.annotate(
            f"{h:{fmt}}",
            (p.get_x() + p.get_width() / 2, h),
            ha="center", va="bottom", fontsize=fontsize, color="#333333",
        )


# ── Q1 ────────────────────────────────────────────────────────────────────────

def plot_score_distributions(
    df: pd.DataFrame,
    save_path: str | None = None,
) -> plt.Figure:
    """
    Q: What does the overall score distribution look like for each subject?
    Shows KDE + histogram for math, reading, and writing scores.
    """
    fig, axes = plt.subplots(1, 3, figsize=(16, 5), sharey=False)
    colors = [PALETTE["primary"], PALETTE["secondary"], PALETTE["accent"]]

    for ax, col, color in zip(axes, SCORE_COLUMNS, colors):
        sns.histplot(df[col], kde=True, ax=ax, color=color,
                     bins=20, edgecolor="white", linewidth=0.5)
        ax.axvline(df[col].mean(), color="red", linestyle="--",
                   linewidth=1.5, label=f"Mean: {df[col].mean():.1f}")
        ax.axvline(df[col].median(), color="black", linestyle=":",
                   linewidth=1.5, label=f"Median: {df[col].median():.1f}")
        ax.set_title(col.replace(" score", "").title() + " Score", fontweight="bold")
        ax.set_xlabel("Score (0–100)")
        ax.set_ylabel("Count")
        ax.legend(fontsize=9)

    fig.suptitle(
        "Q1 · How are student scores distributed across subjects?",
        fontsize=14, fontweight="bold", y=1.01,
    )
    return _save_or_show(fig, save_path)


# ── Q2 ────────────────────────────────────────────────────────────────────────

def plot_gender_comparison(
    df: pd.DataFrame,
    save_path: str | None = None,
) -> plt.Figure:
    """
    Q: Does gender influence academic performance?
    Side-by-side bar chart of average scores by gender.
    """
    avg = df.groupby("gender")[SCORE_COLUMNS].mean().reset_index()
    melted = avg.melt(id_vars="gender", var_name="Subject", value_name="Average Score")
    melted["Subject"] = melted["Subject"].str.replace(" score", "").str.title()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=melted, x="Subject", y="Average Score", hue="gender",
        palette=GENDER_PALETTE, ax=ax, edgecolor="white", linewidth=0.8,
    )
    _add_value_labels(ax)
    ax.set_ylim(0, 85)
    ax.set_title(
        "Q2 · Does gender influence academic performance?\n"
        "Average scores by subject and gender",
        fontweight="bold",
    )
    ax.set_xlabel("")
    ax.legend(title="Gender", title_fontsize=10)
    return _save_or_show(fig, save_path)


# ── Q3 ────────────────────────────────────────────────────────────────────────

def plot_test_prep_impact(
    df: pd.DataFrame,
    save_path: str | None = None,
) -> plt.Figure:
    """
    Q: Does completing a test-preparation course improve scores?
    Box plots comparing score distributions for completed vs none.
    """
    melted = df.melt(
        id_vars=["test preparation course"],
        value_vars=SCORE_COLUMNS,
        var_name="Subject", value_name="Score",
    )
    melted["Subject"] = melted["Subject"].str.replace(" score", "").str.title()

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(
        data=melted, x="Subject", y="Score",
        hue="test preparation course",
        palette={"completed": PALETTE["accent"], "none": PALETTE["highlight"]},
        ax=ax, width=0.5,
    )
    ax.set_title(
        "Q3 · Does test-prep completion boost scores?\n"
        "Score distribution: Completed vs None",
        fontweight="bold",
    )
    ax.set_xlabel("")
    ax.legend(title="Test Prep", title_fontsize=10)
    return _save_or_show(fig, save_path)


# ── Q4 ────────────────────────────────────────────────────────────────────────

def plot_parental_education_effect(
    df: pd.DataFrame,
    save_path: str | None = None,
) -> plt.Figure:
    """
    Q: How does parents' education level relate to student average score?
    Ordered bar chart with error bars (95 % CI).
    """
    from data_cleaner import EDUCATION_ORDER

    order = [e for e in EDUCATION_ORDER if e in df["parental level of education"].unique()]
    avg = (
        df.groupby("parental level of education")["average_score"]
        .agg(["mean", "sem"])
        .reindex(order)
        .reset_index()
    )
    avg.columns = ["Education", "Mean", "SEM"]

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(
        avg["Education"], avg["Mean"],
        color=PALETTE["primary"], edgecolor="white",
        yerr=avg["SEM"] * 1.96, capsize=5, error_kw={"elinewidth": 1.2},
    )
    ax.set_ylim(0, 85)
    for bar, val in zip(bars, avg["Mean"]):
        ax.text(
            bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
            f"{val:.1f}", ha="center", va="bottom", fontsize=9,
        )
    ax.set_xticklabels(avg["Education"], rotation=20, ha="right")
    ax.set_ylabel("Average Score")
    ax.set_title(
        "Q4 · Does parental education level predict student performance?\n"
        "Mean average score with 95% CI",
        fontweight="bold",
    )
    return _save_or_show(fig, save_path)


# ── Q5 ────────────────────────────────────────────────────────────────────────

def plot_lunch_effect(
    df: pd.DataFrame,
    save_path: str | None = None,
) -> plt.Figure:
    """
    Q: Does lunch type (standard vs free/reduced) signal socioeconomic impact?
    Violin plots for each score.
    """
    melted = df.melt(
        id_vars=["lunch"],
        value_vars=SCORE_COLUMNS,
        var_name="Subject", value_name="Score",
    )
    melted["Subject"] = melted["Subject"].str.replace(" score", "").str.title()

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.violinplot(
        data=melted, x="Subject", y="Score", hue="lunch",
        palette={"standard": PALETTE["primary"], "free/reduced": PALETTE["secondary"]},
        ax=ax, split=True, inner="quartile",
    )
    ax.set_title(
        "Q5 · Does lunch type reflect socioeconomic impact on scores?\n"
        "Score distribution: Standard vs Free/Reduced lunch",
        fontweight="bold",
    )
    ax.set_xlabel("")
    ax.legend(title="Lunch Type", title_fontsize=10)
    return _save_or_show(fig, save_path)


# ── Q6 ────────────────────────────────────────────────────────────────────────

def plot_ethnicity_heatmap(
    df: pd.DataFrame,
    save_path: str | None = None,
) -> plt.Figure:
    """
    Q: How do average scores vary across ethnic groups?
    Heatmap: rows = ethnic groups, cols = subjects.
    """
    pivot = (
        df.groupby("race/ethnicity")[SCORE_COLUMNS]
        .mean()
        .rename(columns={c: c.replace(" score", "").title() for c in SCORE_COLUMNS})
        .sort_index()
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.heatmap(
        pivot, annot=True, fmt=".1f", cmap="YlGnBu",
        linewidths=0.5, ax=ax, vmin=60, vmax=80,
        cbar_kws={"label": "Average Score"},
    )
    ax.set_title(
        "Q6 · How do scores vary across ethnic groups?\n"
        "Mean scores by race/ethnicity",
        fontweight="bold",
    )
    ax.set_ylabel("Race / Ethnicity")
    ax.set_xlabel("")
    return _save_or_show(fig, save_path)


# ── Q7 ────────────────────────────────────────────────────────────────────────

def plot_correlation_matrix(
    df: pd.DataFrame,
    save_path: str | None = None,
) -> plt.Figure:
    """
    Q: How strongly are math, reading, and writing skills correlated?
    Annotated correlation heatmap.
    """
    corr = df[SCORE_COLUMNS + ["average_score"]].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        corr, mask=mask, annot=True, fmt=".2f",
        cmap="coolwarm", center=0,
        linewidths=0.5, ax=ax,
        cbar_kws={"label": "Pearson r"},
    )
    ax.set_title(
        "Q7 · Are math, reading, and writing skills correlated?\n"
        "Pearson correlation matrix",
        fontweight="bold",
    )
    return _save_or_show(fig, save_path)


# ── Q8 ────────────────────────────────────────────────────────────────────────

def plot_grade_distribution(
    df: pd.DataFrame,
    save_path: str | None = None,
) -> plt.Figure:
    """
    Q: What fraction of students earn each letter grade?
    Stacked bar by gender.
    """
    grade_order = ["A", "B", "C", "D", "F"]
    counts = (
        df.groupby(["gender", "grade"])
        .size()
        .unstack(fill_value=0)
        .reindex(columns=grade_order, fill_value=0)
    )
    pct = counts.div(counts.sum(axis=1), axis=0) * 100

    fig, ax = plt.subplots(figsize=(10, 6))
    pct.plot(
        kind="bar", stacked=True, ax=ax,
        color=[GRADE_PALETTE[g] for g in grade_order],
        edgecolor="white", linewidth=0.5,
    )
    ax.set_ylabel("Percentage of Students (%)")
    ax.set_xlabel("Gender")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    ax.set_title(
        "Q8 · What share of students achieve each grade, by gender?\n"
        "Grade distribution (stacked %)",
        fontweight="bold",
    )
    ax.legend(title="Grade", bbox_to_anchor=(1.01, 1), loc="upper left")
    return _save_or_show(fig, save_path)


# ── Q9 ────────────────────────────────────────────────────────────────────────

def plot_multi_factor_scatter(
    df: pd.DataFrame,
    save_path: str | None = None,
) -> plt.Figure:
    """
    Q: What combination of factors predicts a high average score?
    Scatter: math vs reading, coloured by test-prep, sized by writing score.
    """
    prep_palette = {"completed": PALETTE["accent"], "none": PALETTE["highlight"]}
    fig, ax = plt.subplots(figsize=(11, 7))

    for prep, grp in df.groupby("test preparation course"):
        ax.scatter(
            grp["math score"], grp["reading score"],
            s=grp["writing score"] * 0.8,
            c=prep_palette[prep], alpha=0.55,
            label=f"Prep: {prep}", edgecolors="white", linewidths=0.3,
        )

    ax.set_xlabel("Math Score")
    ax.set_ylabel("Reading Score")
    ax.set_title(
        "Q9 · What combination of factors leads to high performance?\n"
        "Math vs Reading (bubble size = Writing score, colour = Test prep)",
        fontweight="bold",
    )
    ax.legend(title="Test Prep", title_fontsize=10)
    return _save_or_show(fig, save_path)


# ── Dashboard ────────────────────────────────────────────────────────────────

def plot_executive_dashboard(
    df: pd.DataFrame,
    save_path: str | None = None,
) -> plt.Figure:
    """
    One-page executive dashboard with 4 key KPIs and mini charts.
    Designed to be shared with non-technical stakeholders.
    """
    fig = plt.figure(figsize=(18, 10))
    fig.patch.set_facecolor(PALETTE["bg"])
    gs = fig.add_gridspec(2, 4, hspace=0.45, wspace=0.38)

    # ── KPI tiles ──────────────────────────────────────────────────────────
    kpi_specs = [
        ("Overall Avg Score", f"{df['average_score'].mean():.1f}", PALETTE["primary"]),
        ("Pass Rate (all ≥60)", f"{df['passed_all'].mean()*100:.1f}%", PALETTE["accent"]),
        ("Test-Prep Uplift",
         f"+{df[df['test preparation course']=='completed']['average_score'].mean() - df[df['test preparation course']=='none']['average_score'].mean():.1f} pts",
         PALETTE["secondary"]),
        ("Top Grade (A) Rate", f"{(df['grade']=='A').mean()*100:.1f}%", PALETTE["neutral"]),
    ]
    for i, (label, val, color) in enumerate(kpi_specs):
        ax = fig.add_subplot(gs[0, i])
        ax.set_facecolor(color)
        ax.text(0.5, 0.60, val, ha="center", va="center",
                fontsize=28, fontweight="bold", color="white",
                transform=ax.transAxes)
        ax.text(0.5, 0.22, label, ha="center", va="center",
                fontsize=10, color="white", transform=ax.transAxes)
        ax.set_xticks([]); ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)

    # ── Mini Chart 1: Test Prep effect ────────────────────────────────────
    ax1 = fig.add_subplot(gs[1, 0:2])
    prep_avg = df.groupby("test preparation course")["average_score"].mean()
    ax1.bar(prep_avg.index, prep_avg.values,
            color=[PALETTE["accent"], PALETTE["highlight"]],
            edgecolor="white")
    for bar, val in zip(ax1.patches, prep_avg.values):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height()+0.5,
                 f"{val:.1f}", ha="center", va="bottom", fontsize=10)
    ax1.set_ylim(0, 80)
    ax1.set_title("Test Prep Impact on Avg Score", fontweight="bold")
    ax1.set_xlabel("")

    # ── Mini Chart 2: Lunch type effect ───────────────────────────────────
    ax2 = fig.add_subplot(gs[1, 2:4])
    lunch_avg = df.groupby("lunch")[SCORE_COLUMNS].mean()
    lunch_avg.columns = ["Math", "Reading", "Writing"]
    lunch_avg.T.plot(kind="bar", ax=ax2,
                     color=[PALETTE["primary"], PALETTE["secondary"]],
                     edgecolor="white")
    ax2.set_title("Lunch Type vs Subject Scores", fontweight="bold")
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=0)
    ax2.legend(title="Lunch", fontsize=9)
    ax2.set_ylim(0, 80)

    fig.suptitle(
        "🎓 Student Performance · Executive Dashboard",
        fontsize=16, fontweight="bold", y=1.01,
    )
    return _save_or_show(fig, save_path)
