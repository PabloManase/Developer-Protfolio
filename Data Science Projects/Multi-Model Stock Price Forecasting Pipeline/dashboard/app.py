# --------------------------------------------------------------------------------
# Stock Price Forecasting Dashboard
# Interactive Streamlit dashboard for visualizing historical stock prices
# and generating future price forecasts using machine learning models.
# --------------------------------------------------------------------------------

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from forecast_model import (  # noqa: E402
    load_data,
    train_model,
    add_rolling_stats,
)


# ---------- PAGE CONFIGURATION ----------

# Configure the Streamlit page layout and browser tab title
st.set_page_config(page_title="Stock Forecast Dashboard", layout="wide")
st.title("Stock Price Forecasting Dashboard")


# ---------- SIDEBAR ----------

# User controls
st.sidebar.header("Settings")
forecast_days = st.sidebar.slider("Forecast days", 3, 30, 5)
show_ma = st.sidebar.checkbox("Show moving averages", value=True)
ma_window = st.sidebar.selectbox("MA window", [3, 5, 7, 10], index=1)


# ---------- DATA LOADING & PREPROCESSING ----------

df = load_data()
# Compute rolling statistics (moving avg, std deviation, daily returns)
df = add_rolling_stats(df, windows=[ma_window])
df['Date'] = pd.to_datetime(df['Date'])


# ---------- SUMMARY METRIC CARDS ----------

col1, col2, col3, col4 = st.columns(4)
col1.metric("Latest Price", f"${df['Price'].iloc[-1]:.2f}")
col2.metric("Daily Return", f"{df['Daily_Return'].iloc[-1]:.2f}%")
col3.metric("5-day High", f"${df['Price'].tail(5).max():.2f}")
col4.metric("5-day Low", f"${df['Price'].tail(5).min():.2f}")
st.markdown("---")

# ---------- INTERACTIVE FORECAST CHART ----------

# Build chart
# Layer 1: Historical price data
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df['Date'], y=df['Price'],
    mode='lines+markers', name='Historical Price',
    line=dict(color='#2563EB', width=2)
))
# Layer 2: Moving average overlay
if show_ma and f'MA_{ma_window}' in df.columns:
    fig.add_trace(go.Scatter(
        x=df['Date'], y=df[f'MA_{ma_window}'],
        mode='lines', name=f'{ma_window}-day MA',
        line=dict(color='#7C3AED', dash='dash', width=1.5)
    ))


# ---------- LINEAR REGRESSION FORECAST ----------

# Train the Linear Regression model on a copy of the dataframe
model = train_model(df.copy())

# Generate future day indices starting after the last known data point
future_days = [[len(df) + i] for i in range(1, forecast_days + 1)]
# Predict prices for each future day
lin_preds = model.predict(future_days)

# Build a date range for the forecast period starting after the last known date
last_date = df['Date'].iloc[-1]
future_dates = pd.date_range(last_date, periods=forecast_days+1, freq='D')[1:]

# Layer 3: Forecast line plotted beyond the historical data
fig.add_trace(go.Scatter(
    x=future_dates, y=lin_preds,
    mode='lines+markers', name='Linear Regression Forecast',
    line=dict(color='#059669', dash='dot', width=2)
))
# Chart layout and styling
fig.update_layout(
    title="Price History & Forecast",
    xaxis_title="Date",
    yaxis_title="Price ($)",
    hovermode='x unified',
    height=450
)
st.plotly_chart(fig, use_container_width=True)


# ---------- FORECAST TABLE ----------

st.subheader("Forecast Table")
# Build a structured DataFrame mapping each future date to its predicted price
forecast_df = pd.DataFrame({
    'Date': future_dates.strftime('%Y-%m-%d'),
    'Linear Regression ($)': [f"{p:.2f}" for p in lin_preds],
})
st.dataframe(forecast_df, use_container_width=True)
