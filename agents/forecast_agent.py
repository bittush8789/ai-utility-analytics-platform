import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from utils.groq_client import call_llm

def get_forecast(df, value_col, date_col, periods=30):
    """Simple forecasting using Holt-Winters Exponential Smoothing"""
    try:
        # Prepare data
        df = df.sort_values(by=date_col)
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.set_index(date_col)
        
        # Resample to daily if needed
        ts = df[value_col].resample('D').sum().fillna(0)
        
        # Fit model
        model = ExponentialSmoothing(ts, trend='add', seasonal=None, initialization_method="estimated")
        fit_model = model.fit()
        
        # Forecast
        forecast = fit_model.forecast(periods)
        
        # Return as dataframe
        forecast_df = pd.DataFrame({
            'Date': forecast.index,
            'Forecast': np.round(forecast.values, 2)
        })
        return forecast_df
    except Exception as e:
        return pd.DataFrame({'Date': pd.date_range(start=pd.Timestamp.today(), periods=periods), 'Forecast': 0})

def generate_forecast_insights(kpi_data, periods=30):
    system_prompt = "You are a forecasting expert for a UK Water Utility company."
    prompt = f"Here is the recent KPI trend data:\n{kpi_data}\n\nBased on this, what is your expert narrative forecast for the next {periods} days? What trends do you expect for incidents, complaints, and revenue? Keep it concise and professional (max 3 paragraphs)."
    return call_llm(prompt, system_prompt=system_prompt)
