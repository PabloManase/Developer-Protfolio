# --------------------------------------------------------------------------------
# Core Forecasting Module
# Handles data loading, feature engineering, model training, evaluation,
# ARIMA forecasting, trend analysis, and forecast visualisation.
# --------------------------------------------------------------------------------

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import MinMaxScaler
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
from feature_engineering import build_features


def load_data():
    """
        Load stock price dataset from CSV file.

        Returns:
            pandas.DataFrame - DataFrame containing stock price data.
    """
    # Read CSV file from the data directory
    data = pd.read_csv("data/stock_prices.csv")

    return data


def add_rolling_stats(df, windows=[3, 5, 7]):
    """
        Add moving averages and rolling volatility to the dataframe.

        Parameters:
            df : pandas.DataFrame - stock data with 'Price' column
            windows : list - window sizes in days

        Returns:
            pandas.DataFrame - original df plus new stat columns
    """
    df = df.copy()

    for w in windows:
        # Moving average: smooths out daily noise
        df[f'MA_{w}'] = df['Price'].rolling(window=w).mean()

        # Rolling std deviation: measures price volatility
        df[f'STD_{w}'] = df['Price'].rolling(window=w).std()

    # Price momentum: change over last 3 days
    df['Momentum'] = df['Price'].diff(3)

    # Percentage daily return
    df['Daily_Return'] = df['Price'].pct_change() * 100

    return df


def train_model(df, test_size=0.2):
    """
        Train a Linear Regression model with a proper train/test split.

        Parameters:
            df : pandas.DataFrame - stock data
            test_size : float - fraction of data reserved
                for testing (0.2 - 20%)

        Returns:
            tuple: (fitted model, X_test, y_test) - model + held-out test data
    """
    df['Day'] = range(1, len(df) + 1)
    X = df[['Day']]
    y = df['Price']

    # Split: 80% train, 20% test — shuffle=False preserves time order
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, shuffle=False
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    print(f"Training on {len(X_train)} rows, testing on {len(X_test)} rows")

    return model, X_test, y_test


def train_model_scaled(df, test_size=0.2):
    """
        Train a Linear Regression model with feature scaling applied.
        Scaling ensures no single feature dominates
        just because of its numeric range.

        Parameters:
            df : pandas.DataFrame - stock data
            test_size : float - fraction of data reserved for testing

        Returns:
            tuple: (model, X_test_scaled, y_test,
            feature_scaler, target_scaler)
    """
    df = df.copy()
    df['Day'] = range(1, len(df) + 1)

    feature_cols = ['Day']
    if 'MA_5' in df.columns:
        feature_cols.append('MA_5')

        # Drop NaN rows introduced by the 5-day rolling window
        df = df.dropna()

    X = df[feature_cols].values
    y = df['Price'].values.reshape(-1, 1)

    # Scale both features and target to the [0, 1] range
    feature_scaler = MinMaxScaler()
    target_scaler = MinMaxScaler()

    X_scaled = feature_scaler.fit_transform(X)
    y_scaled = target_scaler.fit_transform(y)

    # Manual time-ordered split - no shuffle to preserve sequence
    split = int(len(X_scaled) * (1 - test_size))
    X_train, X_test = X_scaled[:split], X_scaled[split:]
    y_train, y_test = y_scaled[:split], y_scaled[split:]

    model = LinearRegression()
    model.fit(X_train, y_train.ravel())

    return model, X_test, y_test, feature_scaler, target_scaler


def train_arima(df):
    """
        Train an ARIMA forecasting model.
        ARIMA(p,d,q): p=autoregressive, d=differencing, q=moving average.

        Parameters:
            df : pandas.DataFrame — stock price data

        Returns:
            ARIMAResults — fitted ARIMA model
    """
    # Order (2,1,2) suits short time series — use auto_arima for larger data
    model = ARIMA(df['Price'], order=(2, 1, 2))
    fitted = model.fit()

    return fitted


def forecast_arima(fitted_model, steps=5):
    """
        Generate forecasts from a fitted ARIMA model.

        Parameters:
            fitted_model - result of train_arima()
            steps : int - number of future days to forecast

        Returns:
            pandas.Series — predicted future prices
    """
    forecast = fitted_model.forecast(steps=steps)

    return forecast


def forecast(model):
    """
        Predict future stock prices using the trained Linear Regression model.

        Parameters:
            model : LinearRegression - trained forecasting model

        Returns:
            numpy.ndarray - predicted future stock prices
    """
    # Future day indices continuing from the last training day
    future_days = [[16], [17], [18], [19], [20]]

    # Generate predictions for each future day
    predictions = model.predict(future_days)

    return predictions


def analyze_trends(df):
    """
        Decompose the price series into trend, seasonality, and residual.
        Requires at least 2 full seasonal cycles in the data.

        Parameters:
            df : pandas.DataFrame - stock data with 'Price' column
    """
    # Additive model assumes trend and seasonality add together
    decomposition = seasonal_decompose(
        df['Price'],
        model='additive',
        period=5,                  # 5-day working week cycle
        extrapolate_trend='freq'
    )

    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid

    # Determine overall price direction from first to last trend value
    trend_direction = (
        'Upward' if trend.iloc[-1] > trend.iloc[0] else 'Downward'
    )

    # Measure the spread of seasonal variation across the week
    seasonality_range = seasonal.max() - seasonal.min()

    print("\n=== Trend Analysis ===")
    print(f"Overall trend direction: {trend_direction}")
    print(
        f"Average weekly seasonality range: {seasonality_range:.2f}"
    )
    print(f"Residual std deviation (noise): {residual.std():.4f}")

    # Flag days where residual noise exceeds 2 standard deviations
    vol_threshold = residual.std() * 2
    high_vol_days = df[residual.abs() > vol_threshold]['Date'].tolist()
    print(
        f"High volatility days: "
        f"{high_vol_days if high_vol_days else 'None detected'}"
    )


def evaluate_model(model, X_test, y_test):
    """
        Measure how accurately the model predicts the held-out test data.

        RMSE - Root Mean Squared Error (penalises large errors more)
        MAE  - Mean Absolute Error (average dollar error per prediction)
        R²   - How much variance the model explains (1.0 - perfect)

        Parameters:
            model - fitted LinearRegression model
            X_test, y_test - the held-out 20% of data

        Returns:
            dict - {'rmse', 'mae', 'r2'} scores
    """
    y_pred = model.predict(X_test)

    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = model.score(X_test, y_test)

    print("\n=== Model Evaluation ===")
    print(f"RMSE  : {rmse:.4f}  (avg error in $ terms, squared)")
    print(f"MAE   : {mae:.4f}  (avg dollar error per prediction)")
    print(f"R²    : {r2:.4f}  (1.0 = perfect, 0.0 = no better than mean)")

    return {'rmse': rmse, 'mae': mae, 'r2': r2}


def plot_forecast(df, linear_preds, arima_preds=None):
    """
        Plot historical prices and model forecasts side by side.

        Parameters:
            df : pandas.DataFrame - historical stock data
            linear_preds : array - predictions from linear regression
            arima_preds : array (optional) - predictions from ARIMA
    """
    df['Date'] = pd.to_datetime(df['Date'])
    fig, ax = plt.subplots(figsize=(12, 6))

    # Layer 1: Historical closing prices
    ax.plot(
        df['Date'], df['Price'], 'o-',
        color='#2563EB', label='Historical',
        linewidth=2, markersize=5
    )

    # Layer 2: 5-day moving average overlay (if available)
    if 'MA_5' in df.columns:
        ax.plot(
            df['Date'], df['MA_5'], '--',
            color='#7C3AED', label='5-day MA',
            linewidth=1.5, alpha=0.7
        )

    # Build future date range starting the day after the last known date
    last_date = df['Date'].iloc[-1]
    future_dates = pd.date_range(
        last_date, periods=len(linear_preds) + 1, freq='D'
    )[1:]

    # Layer 3: Linear regression forecast line
    ax.plot(
        future_dates, linear_preds, 's--',
        color='#059669', label='Linear Regression',
        linewidth=2, markersize=6
    )

    # Layer 4: ARIMA forecast line (if provided)
    if arima_preds is not None:
        ax.plot(
            future_dates, arima_preds.values, '^--',
            color='#DC2626', label='ARIMA',
            linewidth=2, markersize=6
        )

    ax.set_title('Stock Price Forecast - Model Comparison', fontsize=14)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price ($)')

    # Format x-axis ticks as readable month/day labels
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('forecast_chart.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("Chart saved to forecast_chart.png")


def main():
    """
        Main program execution function.

        Workflow:
        1. Load dataset
        2. Build engineered features
        3. Compute rolling statistics
        4. Train Linear Regression model
        5. Evaluate model performance
        6. Generate and display forecasts
        7. Run ARIMA forecast
        8. Plot model comparison chart
    """

    # Load raw stock price data from CSV
    df = load_data()
    # Apply feature engineering pipeline (lags, MAs, momentum, etc.)
    df = build_features(df)
    # Compute and display rolling statistics summary
    df = add_rolling_stats(df)
    print(df[['Date', 'Price', 'MA_3', 'MA_5', 'Daily_Return']].to_string())
    # Train Linear Regression on 80% of data, hold out 20% for evaluation
    model, X_test, y_test = train_model(df)
    # Print RMSE, MAE, and R² against the held-out test set
    evaluate_model(model, X_test, y_test)
    # Generate future price predictions using the trained model
    predictions = forecast(model)

    print("\n===================================")
    print(" Future Stock Price Forecast")
    print("===================================\n")

    for i, prediction in enumerate(predictions, start=16):
        print(f"Predicted Price for Day {i}: {prediction:.2f}")

    print("\nForecasting Complete.")

    # Train and run ARIMA model for comparison
    arima_model = train_arima(df)
    arima_preds = forecast_arima(arima_model)

    print("\n=== ARIMA Forecast ===")

    for i, val in enumerate(arima_preds, start=16):
        print(f"Day {i}: {val:.2f}")

    # Render the side-by-side forecast comparison chart
    plot_forecast(df, predictions, arima_preds)


# Program entry point
if __name__ == "__main__":
    main()
