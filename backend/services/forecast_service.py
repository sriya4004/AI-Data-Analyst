import logging
import pandas as pd
from prophet import Prophet
from typing import Dict, Any
from services.forecast_validator import ForecastValidator
from services.data_loader import DataLoader

logger = logging.getLogger(__name__)

class ForecastService:
    """
    Service for performing time-series forecasting using Facebook Prophet.
    """

    @staticmethod
    def generate_forecast(dataset_name: str, date_column: str, target_column: str, periods: int = 30) -> Dict[str, Any]:
        try:
            file_path = f"backend/uploads/{dataset_name}"
            try:
                df = DataLoader.load_dataset(file_path)
            except Exception as e:
                return {"status": "error", "error": f"Failed to read dataset: {e}"}

            validation = ForecastValidator.validate_dataset(df, date_column, target_column)
            if not validation["is_valid"]:
                return {
                    "status": "error",
                    "error": validation["message"],
                    "details": validation.get("details", {}),
                    "error_type": validation.get("error_type")
                }

            forecast_df = ForecastValidator.prepare_prophet_df(df, date_column, target_column)
            if forecast_df.empty:
                return {"status": "error", "error": "Dataset empty after processing."}

            model = Prophet()
            model.fit(forecast_df)

            future = model.make_future_dataframe(periods=periods)
            forecast = model.predict(future)

            result_df = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
            records = result_df.to_dict(orient='records')
            
            for record in records:
                record['ds'] = record['ds'].isoformat()

            return {
                "status": "success",
                "dataset": dataset_name,
                "target_column": target_column,
                "forecast": records
            }

        except Exception as e:
            logger.error(f"Forecast error for {dataset_name}: {e}")
            return {"status": "error", "dataset": dataset_name, "error": str(e)}

forecast_service = ForecastService()
generate_forecast = forecast_service.generate_forecast
