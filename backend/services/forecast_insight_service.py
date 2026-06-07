import logging
from typing import List, Dict, Any
from services.llm_service import generate_response

logger = logging.getLogger(__name__)

class ForecastInsightService:
    """
    Service for generating natural-language business insights from forecast data.
    """

    @staticmethod
    def analyze_trend(forecast_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not forecast_records or len(forecast_records) < 2:
            return {"trend": "stable", "change_pct": 0, "is_significant": False}

        yhat_values = [r['yhat'] for r in forecast_records]
        start_val = yhat_values[0]
        end_val = yhat_values[-1]
        
        change_pct = (end_val - start_val) / abs(start_val) if start_val != 0 else 0

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
    def generate_insight(dataset_name: str, target_column: str, forecast_records: List[Dict[str, Any]]) -> str:
        trend_info = ForecastInsightService.analyze_trend(forecast_records)
        
        prompt = f"""
        You are an expert Business Intelligence Analyst.
        
        Based on the following forecast data for '{target_column}' in '{dataset_name}', 
        generate a single, impactful natural-language business insight.

        Trend Analysis:
        - Detected Trend: {trend_info['trend']}
        - Percentage Change: {trend_info['change_pct']}%
        - Start Value: {trend_info['start_val']}
        - End Value: {trend_info['end_val']}

        Requirements:
        - Concise (one or two sentences).
        - Professional terminology.
        - Contextualized for stakeholders.
        """
        
        try:
            return generate_response(prompt).strip()
        except Exception as e:
            logger.error(f"Failed to generate insight: {e}")
            if trend_info['trend'] == "upward":
                return f"{target_column} is expected to increase by {trend_info['change_pct']}%."
            elif trend_info['trend'] == "downward":
                return f"The forecast indicates a downward trend for {target_column} ({trend_info['change_pct']}%)."
            return f"The prediction for {target_column} remains stable."

forecast_insight_service = ForecastInsightService()
