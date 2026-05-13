import logging
import pandas as pd
from typing import Dict, Any, Optional
from backend.services.forecast_service import generate_forecast
from backend.services.forecast_insight_service import forecast_insight_service
from backend.services.forecast_chart_service import forecast_chart_service
from backend.services.data_loader import DataLoader
from backend.services.auto_column_detection_service import auto_column_detection_service

# Configure logging
logger = logging.getLogger(__name__)

def run_forecast_agent(
    dataset_name: str, 
    date_column: Optional[str] = None, 
    target_column: Optional[str] = None,
    question: Optional[str] = ""
) -> Dict[str, Any]:
    """
    Intelligent Forecast Agent that orchestrates forecasting.
    Supports automatic column detection if they are not provided.
    """
    logger.info(f"Forecast Agent triggered for dataset: {dataset_name}")

    # 1. Validation
    if not dataset_name:
        return {"status": "error", "agent": "Forecast Agent", "message": "dataset_name is required."}

    # 2. Automatic Column Detection if missing
    detected_date = None
    detected_target = None
    
    if not date_column or not target_column:
        logger.info("Columns missing. Attempting automatic detection...")
        try:
            file_path = f"backend/uploads/{dataset_name}"
            df = DataLoader.load_dataset(file_path)
            
            if not date_column:
                date_column = auto_column_detection_service.detect_date_column(df)
                detected_date = date_column
                logger.info(f"Auto-detected date column: {date_column}")
                
            if not target_column:
                target_column = auto_column_detection_service.detect_target_column(df, question)
                detected_target = target_column
                logger.info(f"Auto-detected target column: {target_column}")
                
        except Exception as e:
            logger.error(f"Automatic detection failed: {str(e)}")
            return {
                "status": "error",
                "agent": "Forecast Agent",
                "message": f"Could not auto-detect columns and they were not provided: {str(e)}"
            }

    # Final check after detection attempt
    if not date_column or not target_column:
        error_msg = f"Forecasting requires date and target columns. (Detected: date={date_column}, target={target_column})"
        logger.warning(f"Forecast Agent Error: {error_msg}")
        return {"status": "error", "agent": "Forecast Agent", "message": error_msg}

    try:
        # 3. Generate Forecast Data
        forecast_result = generate_forecast(
            dataset_name=dataset_name,
            date_column=date_column,
            target_column=target_column,
            periods=30
        )

        # 4. Check for service-level errors
        if forecast_result.get("status") == "error":
            return {
                "status": "error",
                "agent": "Forecast Agent",
                "message": forecast_result.get("error", "An unknown error occurred in Forecast Service.")
            }

        forecast_data = forecast_result.get("forecast", [])

        # 5. Generate Business Insights
        insight = forecast_insight_service.generate_insight(
            dataset_name=dataset_name,
            target_column=target_column,
            forecast_records=forecast_data
        )

        # 6. Generate Frontend Chart Configuration
        chart_config = forecast_chart_service.generate_chart_config(
            forecast_records=forecast_data,
            target_column=target_column
        )

        # 7. Return comprehensive structured response
        logger.info(f"Forecast Agent successfully completed for {target_column}")
        return {
            "status": "success",
            "agent": "Forecast Agent",
            "dataset": dataset_name,
            "target_column": target_column,
            "date_column": date_column,
            "detected_date_column": detected_date,
            "detected_target_column": detected_target,
            "forecast": forecast_data,
            "insight": insight,
            "chart_config": chart_config,
            "message": f"Forecast generated successfully for {target_column}."
        }

    except Exception as e:
        logger.exception("Forecast Agent encountered an unexpected internal error.")
        return {
            "status": "error",
            "agent": "Forecast Agent",
            "message": f"Internal Agent Error: {str(e)}"
        }
