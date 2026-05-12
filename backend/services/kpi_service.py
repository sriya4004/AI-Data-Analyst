import pandas as pd


def extract_kpis(query_result):

    if not query_result:

        return {}

    df = pd.DataFrame(query_result)

    kpis = {}

    for column in df.columns:

        if pd.api.types.is_numeric_dtype(df[column]):

            kpis[column] = {
                "mean": float(df[column].mean()),
                "max": float(df[column].max()),
                "min": float(df[column].min())
            }

    return kpis