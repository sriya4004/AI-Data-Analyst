import pandas as pd
import logging
from typing import Dict, Any, Optional

# Configure logging
logger = logging.getLogger(__name__)

class ForecastValidationError(Exception):
    """Custom exception for forecasting validation failures."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.details = details or {}

class ForecastValidator:
    """
    Enterprise-grade validation utilities for forecasting tasks.
    Ensures data integrity and prevents Prophet execution failures.
    """

    @staticmethod
    def validate_dataset(
        df: pd.DataFrame, 
        date_column: str, 
        target_column: str
    ) -> Dict[str, Any]:
        """
        Validates the dataset against forecasting requirements.
        
        Returns:
            Dict containing validation status and details.
        """
        try:
            # 1. Check if dataset is empty or None
            if df is None or df.empty:
                raise ForecastValidationError("The provided dataset is empty or could not be loaded.")

            # 2. Check for column existence
            missing_cols = []
            if date_column not in df.columns:
                missing_cols.append(date_column)
            if target_column not in df.columns:
                missing_cols.append(target_column)
            
            if missing_cols:
                raise ForecastValidationError(
                    f"Required columns missing: {', '.join(missing_cols)}",
                    {"missing_columns": missing_cols}
                )

            # 3. Numeric validation for target column
            # We try to convert a sample to see if it's numeric-compatible
            sample_target = df[target_column].dropna()
            if sample_target.empty:
                 raise ForecastValidationError(f"Target column '{target_column}' is completely empty.")
            
            try:
                pd.to_numeric(sample_target.head(100))
            except (ValueError, TypeError):
                raise ForecastValidationError(
                    f"Target column '{target_column}' must be numeric.",
                    {"current_type": str(df[target_column].dtype)}
                )

            # 4. Datetime validation for date column
            sample_dates = df[date_column].dropna()
            if sample_dates.empty:
                raise ForecastValidationError(f"Date column '{date_column}' is completely empty.")
                
            try:
                pd.to_datetime(sample_dates.head(100))
            except (ValueError, TypeError):
                raise ForecastValidationError(
                    f"Date column '{date_column}' must contain valid date/time strings.",
                    {"column": date_column}
                )

            # 5. Data density validation (Prophet requirement)
            clean_df = df[[date_column, target_column]].dropna()
            if len(clean_df) < 2:
                raise ForecastValidationError(
                    "Insufficient data for forecasting. Minimum 2 non-null rows required.",
                    {"clean_row_count": len(clean_df)}
                )

            logger.info(f"Forecasting validation passed for {target_column}")
            return {
                "is_valid": True,
                "status": "success",
                "message": "Dataset validated successfully."
            }

        except ForecastValidationError as ve:
            logger.warning(f"Validation Error: {str(ve)}")
            return {
                "is_valid": False,
                "status": "error",
                "error_type": "validation_failure",
                "message": str(ve),
                "details": ve.details
            }
        except Exception as e:
            logger.exception("Unexpected error during forecasting validation.")
            return {
                "is_valid": False,
                "status": "error",
                "error_type": "system_failure",
                "message": f"An internal error occurred during validation: {str(e)}"
            }

    @staticmethod
    def prepare_prophet_df(
        df: pd.DataFrame, 
        date_column: str, 
        target_column: str
    ) -> pd.DataFrame:
        """
        Converts a validated dataframe into Prophet's required 'ds' and 'y' format.
        """
        # Create a copy with only needed columns
        df_prophet = df[[date_column, target_column]].copy()
        
        # Rename columns to Prophet standards
        df_prophet = df_prophet.rename(columns={
            date_column: 'ds',
            target_column: 'y'
        })
        
        # Final type enforcement
        df_prophet['ds'] = pd.to_datetime(df_prophet['ds'])
        df_prophet['y'] = pd.to_numeric(df_prophet['y'], errors='coerce')
        
        # Remove any rows that became invalid during conversion (e.g. invalid dates)
        return df_prophet.dropna(subset=['ds', 'y'])
