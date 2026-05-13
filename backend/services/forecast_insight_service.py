import logging
from typing import List, Dict, Any
from backend.services.llm_service import generate_response

# Configure logging
logger = logging.getLogger(__name__)

class ForecastInsightService:
    """
    A service dedicated to generating natural-language business insights
    from forecast data.
    """

    @staticmethod
    def analyze_trend(forecast_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyzes the trend of the forecast data.
        
        Detects:
        - upward trend
        - downward trend
        - stable trend
        """
        if not forecast_records or len(forecast_records) < 2:
            return {
                "trend": "stable",
                "change_pct": 0,
                "is_significant": False
            }

        # We focus on the future part of the forecast (the last segment)
        # Assuming the records are ordered by date
        yhat_values = [r['yhat'] for r in forecast_records]
        
        start_val = yhat_values[0]
        end_val = yhat_values[-1]
        
        if start_val == 0:
            change_pct = 0
        else:
            change_pct = (end_val - start_val) / abs(start_val)

        # Thresholds for significance (e.g., 2% change)
        if change_pct > 0.02:
            trend = "upward"
        elif change_pct < -0.02:
            trend = "downward"
        else:
            trend = "stable"

        return {
            "trend": trend,
            "change_pct": round(change_pct * 100, 2),
            "start_val": round(start_val, 2),
            "end_val": round(end_val, 2),
            "is_significant": abs(change_pct) > 0.02
        }

    @staticmethod
    def generate_insight(
        dataset_name: str,
        target_column: str,
        forecast_records: List[Dict[str, Any]]
    ) -> str:
        """
        Generates a human-readable business insight based on the trend analysis.
        """
        trend_info = ForecastInsightService.analyze_trend(forecast_records)
        
        # Use LLM to generate a professional insight based on the detected trend
        prompt = f"""
        You are an expert Business Intelligence Analyst.
        
        Based on the following forecast data for '{target_column}' in the dataset '{dataset_name}', 
        generate a single, impactful natural-language business insight.

        Trend Analysis:
        - Detected Trend: {trend_info['trend']}
        - Percentage Change: {trend_info['change_pct']}%
        - Starting Forecast Value: {trend_info['start_val']}
        - Ending Forecast Value: {trend_info['end_val']}

        Requirements:
        - Be concise (one or two sentences).
        - Use professional terminology (e.g., "expected to increase", "indicates a downward trend", "stable projection").
        - Contextualize the insight for a business stakeholder.
        
        Example outputs:
        - "Revenue is expected to increase over the next 30 days based on the upward trend."
        - "The forecast indicates a downward sales trend, suggesting a potential decline in volume."
        - "Prediction for user engagement remains stable with no significant fluctuations expected."

        Insight:
        """
        
        try:
            insight = generate_response(prompt)
            return insight.strip()
        except Exception as e:
            logger.error(f"Failed to generate forecast insight: {str(e)}")
            # Fallback to a rule-based template if LLM fails
            if trend_info['trend'] == "upward":
                return f"{target_column} is expected to increase by approximately {trend_info['change_pct']}%."
            elif trend_info['trend'] == "downward":
                return f"The forecast indicates a downward trend for {target_column} ({trend_info['change_pct']}%)."
            else:
                return f"The prediction for {target_column} remains stable for the forecasted period."

# Reusable instance
forecast_insight_service = ForecastInsightService()
