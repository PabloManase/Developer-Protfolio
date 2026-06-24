import pandas as pd


def build_features(df):
    """
        Create a rich feature set from raw price data.
        Each feature gives the model a different signal about price behavior.

        Parameters:
            df : pandas.DataFrame - with 'Date' and 'Price' columns

        Returns:
            pandas.DataFrame - original data plus all engineered features
    """
    
    df = df.copy()
    df['Date'] = pd.to_datetime(df['Date'])

    # Trend features
    df['Day'] = range(1, len(df) + 1)
    df['MA_3'] = df['Price'].rolling(3).mean()
    df['MA_5'] = df['Price'].rolling(5).mean()
    df['MA_7'] = df['Price'].rolling(7).mean()
    # EMA gives more weight to recent prices
    df['EMA_5'] = df['Price'].ewm(span=5, adjust=False).mean()

    #Momentum features
    df['Return_1d'] = df['Price'].pct_change(1)
    df['Return_3d'] = df['Price'].pct_change(3)
    # Measures how far current price sits above or below the 5-day average
    df['Price_vs_MA5'] = df['Price'] / df['MA_5'] - 1

    # Volatility features
    df['Rolling_Std_5'] = df['Price'].rolling(5).std()
    df['Price_Range_5'] = (
        df['Price'].rolling(5).max() - df['Price'].rolling(5).min()
    )

    # Calendar features
    df['DayOfWeek'] = df['Date'].dt.dayofweek  # 0=Mon, 4=Fri
    df['IsMonday'] = (df['DayOfWeek'] == 0).astype(int)
    df['IsFriday'] = (df['DayOfWeek'] == 4).astype(int)

    # Lag features (yesterday's / 2 days ago price)
    df['Lag_1'] = df['Price'].shift(1)
    df['Lag_2'] = df['Price'].shift(2)
    df['Lag_3'] = df['Price'].shift(3)
    # Drop rows with NaN from rolling/lag calculations
    df = df.dropna().reset_index(drop=True)

    return df


def get_feature_columns():
    """
        Return the list of feature column names to pass to your model.
    """
    return [
        'Day', 'MA_3', 'MA_5', 'MA_7', 'EMA_5',
        'Return_1d', 'Return_3d', 'Price_vs_MA5',
        'Rolling_Std_5', 'Price_Range_5',
        'DayOfWeek', 'IsMonday', 'IsFriday',
        'Lag_1', 'Lag_2', 'Lag_3'
    ]


def main():
    """
        Load stock data, apply feature engineering, and display results.
        
        Workflow:
        1. Load raw stock price data from CSV
        2. Apply the full feature engineering pipeline
        3. Print the original vs enriched dataset dimensions
        4. Display the first 5 rows of all engineered features
    """
    df = pd.read_csv("data/stock_prices.csv")
    enriched = build_features(df)
    print(f"Original shape: {df.shape}")
    print(f"Enriched shape: {enriched.shape}")
    print("\nNew features:")
    print(enriched[get_feature_columns()].head(5).to_string())


# Program entry point
if __name__ == "__main__":
    main()
