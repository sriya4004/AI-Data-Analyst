import pandas as pd
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class AutoColumnDetectionService:
    """
    Service for automatically detecting date and target columns from a dataset.
    """

    DATE_KEYWORDS = ["date", "time", "timestamp", "created", "order", "at", "period"]
    TARGET_KEYWORDS = ["sales", "revenue", "profit", "income", "amount", "price", "total", "quantity"]

    @staticmethod
    def detect_date_column(df: pd.DataFrame) -> Optional[str]:
        """
        Detects the best candidate for a date/time column using naming conventions
        and data type verification.
        """
        priority_names = ["date", "order_date", "orderdate", "timestamp", "created_at", "createdat"]
        for name in priority_names:
            for col in df.columns:
                if col.lower() == name:
                    return col

        date_candidates = []
        for col in df.columns:
            if any(key in col.lower() for key in AutoColumnDetectionService.DATE_KEYWORDS):
                sample = df[col].dropna().head(5)
                if not sample.empty:
                    try:
                        pd.to_datetime(sample)
                        date_candidates.append(col)
                    except (ValueError, TypeError):
                        continue

        if date_candidates:
            return date_candidates[0]

        for col in df.columns:
            sample = df[col].dropna().head(5)
            if not sample.empty:
                try:
                    pd.to_datetime(sample)
                    return col
                except (ValueError, TypeError):
                    continue

        return None

    @staticmethod
    def detect_target_column(df: pd.DataFrame, question: str) -> Optional[str]:
        """
        Detects the best candidate for a target forecasting column based on 
        numeric types and keyword matching from the user question.
        """
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if not numeric_cols:
            return None

        question_lower = question.lower()

        for col in numeric_cols:
            if col.lower() in question_lower:
                return col

        for target in AutoColumnDetectionService.TARGET_KEYWORDS:
            for col in numeric_cols:
                if target in col.lower():
                    return col

        for col in numeric_cols:
            if "id" not in col.lower():
                return col

        return numeric_cols[0]

auto_column_detection_service = AutoColumnDetectionService()
