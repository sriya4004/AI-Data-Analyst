import pandas as pd
import os


class DataLoader:

    @staticmethod
    def load_dataset(file_path: str):

        file_extension = os.path.splitext(file_path)[1]

        if file_extension == ".csv":
            df = pd.read_csv(file_path)

        elif file_extension == ".xlsx":
            df = pd.read_excel(file_path)

        else:
            raise ValueError("Unsupported file format")

        return df

    @staticmethod
    def get_preview(df, rows=5):
        preview = df.head(rows)
        preview = preview.astype(object)
        return preview.to_dict(orient="records")

    @staticmethod
    def get_schema(df):

        schema = {}

        for column in df.columns:
            schema[column] = str(df[column].dtype)

        return schema

    @staticmethod
    def get_basic_info(df):

        return {
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1]),
            "column_names": [str(col) for col in df.columns]
        }
        
        
    @staticmethod
    def clean_dataset(df):

        cleaning_report = {
            "duplicates_removed": 0,
            "missing_values_filled": 0
        }

        # Remove duplicates
        initial_rows = len(df)

        df = df.drop_duplicates()

        cleaning_report["duplicates_removed"] = int (
            initial_rows - len(df)
        )

        # Normalize column names
        df.columns = [
            col.strip().lower().replace(" ", "_")
            for col in df.columns
        ]

        # Handle missing values safely
        for column in df.columns:

            missing_before = df[column].isnull().sum()

            # Numeric columns
            if df[column].dtype in ["int64", "float64"]:

                mean_value = df[column].mean()

                df[column] = df[column].fillna(mean_value)

            # Object/string columns
            else:

                df[column] = df[column].fillna("Unknown")

            missing_after = df[column].isnull().sum()

            cleaning_report["missing_values_filled"] += int (
                missing_before - missing_after
            )

        return df, cleaning_report