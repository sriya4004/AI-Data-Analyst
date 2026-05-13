import pandas as pd
import logging
from typing import Optional, List, Tuple

# Configure logging
logger = logging.getLogger(__name__)

class AutoColumnDetectionService:
    """
    Intelligent service to automatically detect date and target columns
    from a dataset based on naming conventions, data types, and user queries.
    """

    DATE_KEYWORDS = ["date", "time", "timestamp", "created", "order", "at", "period"]
    TARGET_KEYWORDS = ["sales", "revenue", "profit", "income", "amount", "price", "total", "quantity"]

    @staticmethod
    def detect_date_column(df: pd.DataFrame) -> Optional[str]:
        """
        Detects the best candidate for a date/time column.
        """
        # 1. Prioritize by exact common names
        priority_names = ["date", "order_date", "orderdate", "timestamp", "created_at", "createdat"]
        for name in priority_names:
            for col in df.columns:
                if col.lower() == name:
                    return col

        # 2. Check for columns containing date keywords and are convertible to datetime
        date_candidates = []
        for col in df.columns:
            col_lower = col.lower()
            if any(key in col_lower for key in AutoColumnDetectionService.DATE_KEYWORDS):
                # Sample a few values to check if they are actually dates
                sample = df[col].dropna().head(5)
                if not sample.empty:
                    try:
                        pd.to_datetime(sample)
                        date_candidates.append(col)
                    except (ValueError, TypeError):
                        continue

        if date_candidates:
            # Return the first one found (or we could refine priority)
            return date_candidates[0]

        # 3. Last resort: check all columns for datetime compatibility
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
        Detects the best candidate for a target forecast column based on 
        numeric type and matching with the user's question.
        """
        # Identify all numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if not numeric_cols:
            return None

        question_lower = question.lower()

        # 1. Check if any numeric column name is mentioned in the user's question
        for col in numeric_cols:
            if col.lower() in question_lower:
                return col

        # 2. Prioritize common forecasting targets
        for target in AutoColumnDetectionService.TARGET_KEYWORDS:
            for col in numeric_cols:
                if target in col.lower():
                    return col

        # 3. Fallback: return the first numeric column that isn't an ID
        for col in numeric_cols:
            if "id" not in col.lower():
                return col

        return numeric_cols[0]

# Reusable instance
auto_column_detection_service = AutoColumnDetectionService()
