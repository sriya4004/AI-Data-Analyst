import pandas as pd
import os

class DataLoader:
    """
    Service for loading, previewing, and cleaning datasets.
    """

    @staticmethod
    def load_dataset(file_path: str):
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension == ".csv":
            return pd.read_csv(file_path)
        elif file_extension == ".xlsx":
            return pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

    @staticmethod
    def get_preview(df, rows=5):
        return df.head(rows).astype(object).to_dict(orient="records")

    @staticmethod
    def get_schema(df):
        return {col: str(dtype) for col, dtype in df.dtypes.items()}

    @staticmethod
    def get_basic_info(df):
        return {
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1]),
            "column_names": [str(col) for col in df.columns]
        }

    @staticmethod
    def clean_dataset(df):
        initial_rows = len(df)
        df = df.drop_duplicates()
        duplicates_removed = int(initial_rows - len(df))

        # Normalize column names
        df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

        missing_values_filled = 0
        for column in df.columns:
            missing_before = df[column].isnull().sum()
            if df[column].dtype in ["int64", "float64"]:
                df[column] = df[column].fillna(df[column].mean())
            else:
                df[column] = df[column].fillna("Unknown")
            missing_after = df[column].isnull().sum()
            missing_values_filled += int(missing_before - missing_after)

        report = {
            "duplicates_removed": duplicates_removed,
            "missing_values_filled": missing_values_filled
        }
        return df, report