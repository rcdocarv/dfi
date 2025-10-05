# pages/utils.py

import pandas as pd

def sanitize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    for c in df.columns:
        if df[c].dtype == "O":
            df[c] = df[c].astype(str)
    return df