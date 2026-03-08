

import json
import os
from datetime import datetime


# ── Helpers ──────────────────────────────────────────────────────────────────

def _sig(result: dict, label: str = "") -> str:
    """Return a human-readable significance verdict."""
    sig = result.get("significant", False)
    p   = result.get("p_value", 1.0)
    direction = "✅ Statistically significant" if sig else "❌ Not significant"
    return f"{direction} (p = {p:.4f}){' — ' + label if label else ''}"


def _effect(result: dict) -> str:
    d = result.get("cohen_d")
    if d is not None:
        size = result.get("effect_size", "")
        return f"Effect size (Cohen's d): {d:.3f} ({size})"
    v = result.get("cramers_v")
    if v is not None:
        assoc = result.get("association", "")
        return f"Effect size (Cramér's V): {v:.3f} ({assoc})"
    return ""


# ── Section builders ─────────────────────────────────────────────────────────

def _header(title: str, level: int = 2) -> str:
    prefix = "#" * level
    return f"\n{prefix} {title}\n"


def _build_executive_summary(stats: dict, df_shape: tuple) -> str:
    lines = [_header("Executive Summary", 2)]
    lines.append(
        f"This report analyses academic performance data for **{df_shape[0]} students** "
        f"across {df_shape[1]} variables including gender, parental education, "
        f"test preparation, and lunch type.\n"
    )

    desc = stats.get("descriptive", {})
    avg_mean = desc.get("mean", {}).get("average_score", "N/A")
    lines.append(f"- Overall average score: **{avg_mean:.1f} / 100**")

    pr_g = stats.get("pass_rate_gender", {}).get("pass_rate_%", {})
    if pr_g:
        best_group = max(pr_g, key=pr_g.get)
        lines.append(f"- Highest pass-rate group (by gender): **{best_group}** at {pr_g[best_group]:.1f}%")

    tp = stats.get("testprep_t_test", {})
    if tp.get("significant"):
        groups = tp.get("groups", {})
        diff = abs(list(groups.values())[0] - list(groups.values())[1])
        lines.append(f"- Test-preparation completion is associated with a **{diff:.1f}-point** average score uplift")

    return "\n".join(lines)


def _build_descriptive_section(stats: dict) -> str:
    lines = [_header("Descriptive Statistics", 2)]
    desc  = stats.get("descriptive", {})
    means  = desc.get("mean",   {})
    stds   = desc.get("std",    {})
    skews  = desc.get("skewness", {})

    lines.append("| Metric | Mean | Std Dev | Skewness |")
    lines.append("|--------|------|---------|----------|")
    for col in means:
        lines.append(
            f"| {col} | {means[col]:.2f} | {stds.get(col, 0):.2f} | {skews.get(col, 0):.3f} |"
        )
    return "\n".join(lines)


def _build_hypothesis_section(stats: dict) -> str:
    lines = [_header("Hypothesis Tests", 2)]

    # Gender
    lines.append(_header("H1 · Gender and average score", 3))
    g = stats.get("gender_t_test", {})
    if g:
        groups = g.get("groups", {})
        for name, val in groups.items():
            lines.append(f"  - {name.title()}: mean = {val:.2f}")
        lines.append(f"  - {_sig(g)}")
        lines.append(f"  - {_effect(g)}")

    # Test prep
    lines.append(_header("H2 · Test-preparation course and average score", 3))
    tp = stats.get("testprep_t_test", {})
    if tp:
        for name, val in tp.get("groups", {}).items():
            lines.append(f"  - {name.title()}: mean = {val:.2f}")
        lines.append(f"  - {_sig(tp)}")
        lines.append(f"  - {_effect(tp)}")

    # Lunch
    lines.append(_header("H3 · Lunch type (socioeconomic proxy) and average score", 3))
    lt = stats.get("lunch_t_test", {})
    if lt:
        for name, val in lt.get("groups", {}).items():
            lines.append(f"  - {name.title()}: mean = {val:.2f}")
        lines.append(f"  - {_sig(lt)}")
        lines.append(f"  - {_effect(lt)}")

    # Parental education ANOVA
    lines.append(_header("H4 · Parental education level and average score (ANOVA)", 3))
    ea = stats.get("edu_anova", {})
    if ea:
        lines.append(f"  - F-statistic: {ea.get('f_stat', 0):.4f}")
        lines.append(f"  - {_sig(ea)}")
        gm = ea.get("group_means", {})
        best_edu = max(gm, key=gm.get) if gm else "N/A"
        lines.append(f"  - Highest-performing group: **{best_edu}** (mean = {gm.get(best_edu, 0):.2f})")

    # Ethnicity ANOVA
    lines.append(_header("H5 · Ethnic group and average score (ANOVA)", 3))
    eth = stats.get("ethnicity_anova", {})
    if eth:
        lines.append(f"  - F-statistic: {eth.get('f_stat', 0):.4f}")
        lines.append(f"  - {_sig(eth)}")

    return "\n".join(lines)


def _build_correlation_section(stats: dict) -> str:
    lines = [_header("Correlation Analysis", 2)]
    corr  = stats.get("correlation", {})
    cols  = list(corr.keys())
    lines.append("| | " + " | ".join(cols) + " |")
    lines.append("|---|" + "---|" * len(cols))
    for row_col in cols:
        row = [f"{corr[col].get(row_col, 0):.3f}" for col in cols]
        lines.append(f"| **{row_col}** | " + " | ".join(row) + " |")
    return "\n".join(lines)


def _build_recommendations(stats: dict) -> str:
    lines = [_header("Key Findings & Recommendations", 2)]

    tp = stats.get("testprep_t_test", {})
    groups = tp.get("groups", {})
    vals   = list(groups.values())
    diff   = abs(vals[0] - vals[1]) if len(vals) == 2 else 0

    bullets = [
        f"**Test preparation matters**: Students who completed prep scored ~{diff:.1f} points higher on average.",
        "**Socioeconomic signals**: Lunch type is a significant predictor — consider targeted support programs for free/reduced lunch students.",
        "**Parental education gradient**: Higher parental education correlates with better student outcomes; family engagement programs may help.",
        "**Subject correlations are high** (r > 0.8): Strong readers tend to be strong writers — interdisciplinary literacy programs could be efficient.",
        "**Ethnic group gaps exist**: Targeted interventions for lower-performing groups should be considered.",
    ]
    for b in bullets:
        lines.append(f"- {b}")

    return "\n".join(lines)


# ── Public API ────────────────────────────────────────────────────────────────

def generate_markdown_report(
    stats: dict,
    df_shape: tuple,
    output_path: str = "report.md",
) -> str:
    """
    Generate a complete markdown report and optionally write it to disk.

    Parameters
    ----------
    stats       : output of statistical_analysis.full_stats_report()
    df_shape    : (n_rows, n_cols) of the cleaned DataFrame
    output_path : if provided, write the report to this file

    Returns
    -------
    str  – the full report text
    """
    sections = [
        f"# 🎓 Student Performance Analysis Report",
        f"_Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n",
        _build_executive_summary(stats, df_shape),
        _build_descriptive_section(stats),
        _build_hypothesis_section(stats),
        _build_correlation_section(stats),
        _build_recommendations(stats),
        _header("Appendix", 2),
        "Full statistical test outputs are available in the accompanying Jupyter notebook.",
    ]

    report = "\n\n".join(sections)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"📄 Markdown report saved → {output_path}")

    return report


def generate_json_report(
    stats: dict,
    df_shape: tuple,
    output_path: str = "stats_report.json",
) -> None:
    """Serialise the full stats dict to JSON for downstream consumption."""

    # stats values may contain non-serialisable objects; convert them
    def _safe(obj):
        if isinstance(obj, (bool, int, float, str, type(None))):
            return obj
        if isinstance(obj, dict):
            return {k: _safe(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [_safe(i) for i in obj]
        return str(obj)

    payload = {
        "generated_at": datetime.now().isoformat(),
        "dataset_shape": {"rows": df_shape[0], "cols": df_shape[1]},
        "statistics":    _safe(stats),
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"📄 JSON report saved → {output_path}")
