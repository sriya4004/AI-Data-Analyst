from typing import List, Dict, Any

class ForecastChartService:
    """
    A service for generating frontend-ready chart configurations 
    specifically for time-series forecasting data.
    """

    @staticmethod
    def generate_chart_config(
        forecast_records: List[Dict[str, Any]], 
        target_column: str
    ) -> Dict[str, Any]:
        """
        Transforms raw forecast records into a structured JSON configuration 
        compatible with modern frontend charting libraries (Chart.js, Recharts, etc.)
        
        Includes:
        - Labels (dates)
        - Predicted values (yhat)
        - Confidence intervals (yhat_lower, yhat_upper)
        """
        if not forecast_records:
            return {
                "error": "No forecast data available to generate chart configuration."
            }

        # Extracting the series
        # We ensure dates are in string format for JSON compatibility
        labels = [str(r['ds']) for r in forecast_records]
        predicted_values = [round(r['yhat'], 2) for r in forecast_records]
        lower_bounds = [round(r['yhat_lower'], 2) for r in forecast_records]
        upper_bounds = [round(r['yhat_upper'], 2) for r in forecast_records]

        # Constructing the frontend-ready configuration
        chart_config = {
            "type": "forecast_chart",
            "title": f"Forecast Projection for {target_column}",
            "xAxis": {
                "label": "Date",
                "data": labels
            },
            "yAxis": {
                "label": target_column
            },
            "datasets": [
                {
                    "id": "prediction",
                    "label": "Predicted Value",
                    "data": predicted_values,
                    "borderColor": "#6366f1",  # Indigo
                    "backgroundColor": "rgba(99, 102, 241, 0.1)",
                    "borderWidth": 3,
                    "pointRadius": 2,
                    "fill": True
                },
                {
                    "id": "confidence_interval",
                    "label": "95% Confidence Interval",
                    "data": [
                        {"low": low, "high": high} 
                        for low, high in zip(lower_bounds, upper_bounds)
                    ],
                    "backgroundColor": "rgba(99, 102, 241, 0.2)",
                    "borderWidth": 0,
                    "fill": True,
                    "isArea": True
                }
            ],
            # Helper for frontends that prefer a combined format for tooltips
            "combinedData": [
                {
                    "date": labels[i],
                    "predicted": predicted_values[i],
                    "lower": lower_bounds[i],
                    "upper": upper_bounds[i]
                }
                for i in range(len(labels))
            ]
        }

        return chart_config

# Reusable instance
forecast_chart_service = ForecastChartService()
