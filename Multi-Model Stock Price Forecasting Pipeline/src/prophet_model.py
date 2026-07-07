# --------------------------------------------------------------------------------
# Prophet Forecasting Module
# Trains and generates stock price forecasts using Facebook Prophet —
# a decomposable model that handles trend, seasonality, and holidays.
# --------------------------------------------------------------------------------


import pandas as pd
from prophet import Prophet


def prepare_prophet_data(df):
    """
        Prophet requires columns named 'ds' (date) and 'y' (value).

        Parameters:
            df : pandas.DataFrame - must have 'Date' and 'Price' columns

        Returns:
            pandas.DataFrame - renamed for Prophet
    """

    # Rename columns to match Prophet's required input format
    prophet_df = df.rename(columns={'Date': 'ds', 'Price': 'y'})

    # Ensure the date column is in datetime format for Prophet to parse
    prophet_df['ds'] = pd.to_datetime(prophet_df['ds'])

    return prophet_df


def train_prophet(prophet_df):
    """
        Train a Prophet forecasting model.

        Parameters:
            prophet_df : pandas.DataFrame - output of prepare_prophet_data()

        Returns:
            Prophet - fitted model
    """

    # Enable daily seasonality to capture intra-week price patterns
    model = Prophet(daily_seasonality=True)
    model.fit(prophet_df)

    return model


def forecast_prophet(model, days=5):
    """
        Generate future predictions with Prophet.

        Parameters:
            model - fitted Prophet model
            days : int - number of future days to forecast

        Returns:
            pandas.DataFrame - contains 'ds', 'yhat',
            'yhat_lower', 'yhat_upper'
    """

    # Extend the dataframe with future dates for the forecast horizon
    future = model.make_future_dataframe(periods=days)

    # Generate point forecasts and confidence intervals
    forecast = model.predict(future)

    return forecast


def main():
    """
        Load stock data, train Prophet model, and print future forecasts.
        
        Workflow:
        1. Load raw stock price data from CSV
        2. Rename columns to Prophet's required format (ds, y)
        3. Train the Prophet forecasting model
        4. Generate forecasts for the next 5 days
        5. Display predicted prices with confidence intervals
    """
    df = pd.read_csv("data/stock_prices.csv")
    prophet_df = prepare_prophet_data(df)
    model = train_prophet(prophet_df)
    forecast = forecast_prophet(model)
    # Display only the forecast columns for the final predicted days
    output_cols = ['ds', 'yhat', 'yhat_lower', 'yhat_upper']
    print("\n=== Prophet Forecast (next 5 days) ===")
    print(forecast[output_cols].tail(5).to_string(index=False))


# Program entry point
if __name__ == "__main__":
    main()
