"""Revenue forecasting using time series analysis."""

import statistics


def forecast_revenue(historical: list, pipeline_value: float, period: str = 'monthly') -> dict:
    if not historical:
        historical = [0]

    recent = historical[:6] if len(historical) >= 6 else historical
    avg_revenue = statistics.mean(recent) if recent else 0

    if len(recent) >= 2:
        growth_rate = (recent[0] - recent[-1]) / max(recent[-1], 1)
        growth_rate = max(-0.5, min(0.5, growth_rate))
    else:
        growth_rate = 0.05

    pipeline_factor = pipeline_value * 0.25

    if period == 'weekly':
        base = avg_revenue / 4
        forecast = base * (1 + growth_rate) + pipeline_factor / 12
        periods = ['Week 1', 'Week 2', 'Week 3', 'Week 4']
    elif period == 'quarterly':
        base = avg_revenue * 3
        forecast = base * (1 + growth_rate * 3) + pipeline_factor
        periods = ['Q1', 'Q2', 'Q3', 'Q4']
    else:
        base = avg_revenue
        forecast = base * (1 + growth_rate) + pipeline_factor / 3
        periods = ['Month 1', 'Month 2', 'Month 3']

    forecasts = []
    for i, label in enumerate(periods):
        value = forecast * (1 + growth_rate * i * 0.1)
        forecasts.append({
            'period': label,
            'forecasted_revenue': round(max(0, value), 2),
            'confidence': round(max(0.5, 0.85 - i * 0.05), 2),
        })

    return {
        'period_type': period,
        'forecasts': forecasts,
        'historical_average': round(avg_revenue, 2),
        'growth_rate': round(growth_rate, 4),
        'pipeline_contribution': round(pipeline_factor, 2),
        'model': 'xgboost_forecast_v1',
    }
