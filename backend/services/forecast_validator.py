import pandas as pd
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ForecastValidationError(Exception):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.details = details or {}

class ForecastValidator:
    """
    Validation utilities for forecasting tasks to ensure data integrity.
    """

    @staticmethod
    def validate_dataset(df: pd.DataFrame, date_column: str, target_column: str) -> Dict[str, Any]:
        try:
            if df is None or df.empty:
                raise ForecastValidationError("The dataset is empty.")

            missing_cols = [col for col in [date_column, target_column] if col not in df.columns]
            if missing_cols:
                raise ForecastValidationError(f"Missing columns: {', '.join(missing_cols)}", {"missing": missing_cols})

            target_sample = df[target_column].dropna()
            if target_sample.empty:
                raise ForecastValidationError(f"Target column '{target_column}' is empty.")
            
            try:
                pd.to_numeric(target_sample.head(100))
            except (ValueError, TypeError):
                raise ForecastValidationError(f"Target column '{target_column}' must be numeric.")

            date_sample = df[date_column].dropna()
            if date_sample.empty:
                raise ForecastValidationError(f"Date column '{date_column}' is empty.")
                
            try:
                pd.to_datetime(date_sample.head(100))
            except (ValueError, TypeError):
                raise ForecastValidationError(f"Date column '{date_column}' must contain valid dates.")

            if len(df[[date_column, target_column]].dropna()) < 2:
                raise ForecastValidationError("Insufficient data. Minimum 2 non-null rows required.")

            return {"is_valid": True, "status": "success", "message": "Validated successfully."}

        except ForecastValidationError as ve:
            return {"is_valid": False, "status": "error", "error_type": "validation_failure", "message": str(ve), "details": ve.details}
        except Exception as e:
            logger.error(f"Validation error: {e}")
            return {"is_valid": False, "status": "error", "error_type": "system_failure", "message": str(e)}

    @staticmethod
    def prepare_prophet_df(df: pd.DataFrame, date_column: str, target_column: str) -> pd.DataFrame:
        df_prophet = df[[date_column, target_column]].copy()
        df_prophet = df_prophet.rename(columns={date_column: 'ds', target_column: 'y'})
        df_prophet['ds'] = pd.to_datetime(df_prophet['ds'])
        df_prophet['y'] = pd.to_numeric(df_prophet['y'], errors='coerce')
        return df_prophet.dropna(subset=['ds', 'y'])
