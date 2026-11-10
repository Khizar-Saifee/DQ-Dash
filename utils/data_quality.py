import pandas as pd
import numpy as np

def calculate_data_quality(df):
    total_cells = df.size
    missing_cells = df.isnull().sum().sum()
    duplicate_rows = df.duplicated().sum()

    completeness = 100 - ((missing_cells / total_cells) * 100)
    uniqueness = 100 - ((duplicate_rows / len(df)) * 100 if len(df) > 0 else 0)

    # Simple weighted score
    quality_score = (0.6 * completeness) + (0.4 * uniqueness)

    return {
        "Total Rows": len(df),
        "Total Columns": df.shape[1],
        "Missing Values": int(missing_cells),
        "Duplicate Rows": int(duplicate_rows),
        "Completeness (%)": round(completeness, 2),
        "Uniqueness (%)": round(uniqueness, 2),
        "Overall Quality Score": round(quality_score, 2)
    }

def detect_outliers(df):
    outlier_counts = {}

    for col in df.select_dtypes(include=['int64', 'float64']).columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        outliers = df[(df[col] < lower) | (df[col] > upper)]
        outlier_counts[col] = len(outliers)

    return outlier_counts

def remove_outliers_iqr(df):
    df_clean = df.copy()

    for col in df_clean.select_dtypes(include=['int64', 'float64']).columns:
        Q1 = df_clean[col].quantile(0.25)
        Q3 = df_clean[col].quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        df_clean = df_clean[
            (df_clean[col] >= lower) &
            (df_clean[col] <= upper)
        ]

    return df_clean
