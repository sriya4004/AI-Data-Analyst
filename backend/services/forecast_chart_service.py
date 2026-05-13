from typing import List, Dict, Any

class ForecastChartService:
    """
    Service for generating frontend-ready chart configurations for forecasting.
    """

    @staticmethod
    def generate_chart_config(forecast_records: List[Dict[str, Any]], target_column: str) -> Dict[str, Any]:
        if not forecast_records:
            return {"error": "No forecast data available."}

        labels = [str(r['ds']) for r in forecast_records]
        yhat = [round(r['yhat'], 2) for r in forecast_records]
        yhat_lower = [round(r['yhat_lower'], 2) for r in forecast_records]
        yhat_upper = [round(r['yhat_upper'], 2) for r in forecast_records]

        return {
            "type": "forecast_chart",
            "title": f"Forecast Projection for {target_column}",
            "xAxis": {"label": "Date", "data": labels},
            "yAxis": {"label": target_column},
            "datasets": [
                {
                    "id": "prediction",
                    "label": "Predicted Value",
                    "data": yhat,
                    "borderColor": "#6366f1",
                    "backgroundColor": "rgba(99, 102, 241, 0.1)",
                    "borderWidth": 3,
                    "pointRadius": 2,
                    "fill": True
                },
                {
                    "id": "confidence_interval",
                    "label": "95% Confidence Interval",
                    "data": [{"low": l, "high": h} for l, h in zip(yhat_lower, yhat_upper)],
                    "backgroundColor": "rgba(99, 102, 241, 0.2)",
                    "borderWidth": 0,
                    "fill": True,
                    "isArea": True
                }
            ],
            "combinedData": [
                {
                    "date": labels[i],
                    "predicted": yhat[i],
                    "lower": yhat_lower[i],
                    "upper": yhat_upper[i]
                }
                for i in range(len(labels))
            ]
        }

forecast_chart_service = ForecastChartService()
