import pandas as pd


def calculate_quality_score(df, report):

    total_cells = df.shape[0] * df.shape[1]

    missing = df.isna().sum().sum()

    duplicates = report["duplicates_removed"]

    score = 100

    score -= duplicates * 0.5

    score -= (missing / max(total_cells, 1)) * 100

    score = max(round(score, 2), 0)

    if score >= 95:
        status = "Excellent"
    elif score >= 85:
        status = "Good"
    elif score >= 70:
        status = "Average"
    else:
        status = "Poor"

    return {
        "score": score,
        "status": status,
        "duplicates": duplicates,
        "missing": int(missing),
    }


def missing_report(df):

    report = (
        df.isna()
        .sum()
        .reset_index()
    )

    report.columns = ["Column", "Missing Values"]

    report["Missing %"] = (
        report["Missing Values"] / len(df) * 100
    ).round(2)

    return report


def datatype_report(df):

    return pd.DataFrame({
        "Column": df.columns,
        "Datatype": df.dtypes.astype(str),
        "Unique Values": [df[c].nunique() for c in df.columns]
    })