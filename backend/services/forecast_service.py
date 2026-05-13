import pandas as pd
from prophet import Prophet
from typing import Dict, Any, List
import logging
from backend.services.forecast_validator import ForecastValidator
from backend.services.data_loader import DataLoader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ForecastService:
    """
    A service class for performing time-series forecasting using Facebook Prophet.
    """

    @staticmethod
    def generate_forecast(
        dataset_name: str, 
        date_column: str, 
        target_column: str, 
        periods: int = 30
    ) -> Dict[str, Any]:
        """
        Generates a time-series forecast for a given dataset and target column.
        """
        try:
            # 1. Retrieve dataset
            file_path = f"backend/uploads/{dataset_name}"
            try:
                df = DataLoader.load_dataset(file_path)
            except Exception as e:
                return {
                    "status": "error",
                    "error": f"Failed to read dataset file: {str(e)}"
                }

            # 2. Comprehensive Validation
            validation_result = ForecastValidator.validate_dataset(
                df, date_column, target_column
            )
            
            if not validation_result["is_valid"]:
                return {
                    "status": "error",
                    "error": validation_result["message"],
                    "details": validation_result.get("details", {}),
                    "error_type": validation_result.get("error_type")
                }

            # 3. Prepare data for Prophet
            forecast_df = ForecastValidator.prepare_prophet_df(
                df, date_column, target_column
            )

            if forecast_df.empty:
                return {
                    "status": "error",
                    "error": "Dataset became empty after date/numeric conversion."
                }

            # 4. Initialize and train the Prophet model
            # We use suppress_stdout_stderr context or logger adjustment if needed, 
            # but standard instantiation is fine for now.
            model = Prophet()
            model.fit(forecast_df)

            # 5. Create future dataframe and generate predictions
            future = model.make_future_dataframe(periods=periods)
            forecast = model.predict(future)

            # 6. Extract relevant results
            result_df = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
            
            # Convert results to a list of records for easy JSON serialization
            # Using ISO format for dates
            records = result_df.to_dict(orient='records')
            for record in records:
                record['ds'] = record['ds'].isoformat()

            logger.info(f"Successfully generated forecast for {dataset_name} ({target_column})")

            return {
                "dataset": dataset_name,
                "target_column": target_column,
                "forecast": records,
                "status": "success"
            }

        except Exception as e:
            logger.error(f"Error generating forecast for {dataset_name}: {str(e)}")
            return {
                "dataset": dataset_name,
                "error": str(e),
                "status": "error"
            }

# Reusable instance
forecast_service = ForecastService()
generate_forecast = forecast_service.generate_forecast
