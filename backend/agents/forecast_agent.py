import logging
from typing import Dict, Any
from backend.services.forecast_service import generate_forecast
from backend.services.forecast_insight_service import forecast_insight_service
from backend.services.forecast_chart_service import forecast_chart_service

# Configure logging
logger = logging.getLogger(__name__)

def run_forecast_agent(
    dataset_name: str, 
    date_column: str, 
    target_column: str
) -> Dict[str, Any]:
    """
    Specialized Forecast Agent that orchestrates forecasting, insight generation,
    and chart configuration.
    """
    logger.info(f"Forecast Agent triggered for dataset: {dataset_name}, target: {target_column}")

    # 1. Validation
    if not dataset_name:
        return {"status": "error", "agent": "Forecast Agent", "message": "dataset_name is required."}
    
    if not date_column or not target_column:
        error_msg = "Both 'date_column' and 'target_column' must be provided for forecasting."
        logger.warning(f"Forecast Agent Validation Error: {error_msg}")
        return {"status": "error", "agent": "Forecast Agent", "message": error_msg}

    try:
        # 2. Generate Forecast Data
        forecast_result = generate_forecast(
            dataset_name=dataset_name,
            date_column=date_column,
            target_column=target_column,
            periods=30
        )

        # 3. Check for service-level errors
        if forecast_result.get("status") == "error":
            return {
                "status": "error",
                "agent": "Forecast Agent",
                "message": forecast_result.get("error", "An unknown error occurred in Forecast Service.")
            }

        forecast_data = forecast_result.get("forecast", [])

        # 4. Generate Business Insights
        insight = forecast_insight_service.generate_insight(
            dataset_name=dataset_name,
            target_column=target_column,
            forecast_records=forecast_data
        )

        # 5. Generate Frontend Chart Configuration
        chart_config = forecast_chart_service.generate_chart_config(
            forecast_records=forecast_data,
            target_column=target_column
        )

        # 6. Return comprehensive structured response
        logger.info(f"Forecast Agent successfully completed for {target_column}")
        return {
            "status": "success",
            "agent": "Forecast Agent",
            "dataset": dataset_name,
            "target_column": target_column,
            "forecast": forecast_data,
            "insight": insight,
            "chart_config": chart_config,
            "message": f"Forecast, insights, and chart config generated successfully for {target_column}."
        }

    except Exception as e:
        logger.exception("Forecast Agent encountered an unexpected internal error.")
        return {
            "status": "error",
            "agent": "Forecast Agent",
            "message": f"Internal Agent Error: {str(e)}"
        }
