import pandas as pd
import numpy as np

def remove_duplicates(df):
    return df.drop_duplicates()

def fill_missing(df, method="mean"):
    df_clean = df.copy()

    for col in df_clean.columns:
        if np.issubdtype(df_clean[col].dtype, np.number):
            if method == "mean":
                df_clean[col] = df_clean[col].fillna(
                    df_clean[col].mean()
                )
            elif method == "median":
                df_clean[col] = df_clean[col].fillna(
                    df_clean[col].median()
                )
        else:
            df_clean[col] = df_clean[col].fillna("Unknown")

    return df_clean