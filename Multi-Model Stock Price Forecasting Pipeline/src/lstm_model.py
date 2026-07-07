# --------------------------------------------------------------------------------
# LSTM Forecasting Module
# Builds, trains, and forecasts stock prices using a Long Short-Term Memory
# (LSTM) recurrent neural network implemented in Keras.
# --------------------------------------------------------------------------------


import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential  # noqa: E402
from keras.layers import LSTM, Dense  # noqa: E402


def prepare_lstm_data(df, look_back=3):
    """
        Convert price series into supervised learning format.
        'look_back' means: use 3 previous days to predict the next day.

        Parameters:
            df : pandas.DataFrame - stock data
            look_back : int - number of previous days used as features

        Returns:
            X, y arrays and the scaler object (needed to reverse scaling)
    """

    # Scale prices to the range [0, 1] — required for stable LSTM training
    scaler = MinMaxScaler(feature_range=(0, 1))
    prices = scaler.fit_transform(df[['Price']])

    # Build sliding windows: each X[i] is look_back days, y[i] is the next day
    X, y = [], []
    for i in range(look_back, len(prices)):
        X.append(prices[i - look_back:i, 0])
        y.append(prices[i, 0])

    # Reshape X to (samples, timesteps, features) as required by Keras LSTM
    X = np.array(X).reshape(-1, look_back, 1)
    y = np.array(y)

    return X, y, scaler


def build_lstm(look_back=3):
    """
        Build a simple 2-layer LSTM network.

        Returns:
            keras.Sequential - compiled model ready to train
    """

    # Stack 2 LSTM layers and single Dense output neuron
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(look_back, 1)),
        LSTM(50),
        Dense(1)
    ])

    # Adam optimizer with MSE loss is standard for regression tasks
    model.compile(optimizer='adam', loss='mean_squared_error')

    return model


def train_lstm(model, X, y, epochs=50):
    """
        Train the LSTM model.

        Parameters:
            model - output of build_lstm()
            X, y - output of prepare_lstm_data()
            epochs : int - training iterations (increase for more data)
        Returns:
            keras.Sequential - trained model
    """

    # batch_size=1 (online learning) suits small datasets like this one
    model.fit(X, y, epochs=epochs, batch_size=1, verbose=0)

    return model


def forecast_lstm(model, df, scaler, look_back=3, steps=5):
    """
        Use the trained LSTM to predict future prices.

        Parameters:
            model - trained LSTM model
            df : pandas.DataFrame - original stock data
            scaler - fitted MinMaxScaler used during training
            look_back : int - window size used during training
            steps : int - number of future days to predict

        Returns:
            numpy.ndarray - predicted prices in original dollar scale
    """

    # Scale the full price series using the already-fitted scaler
    prices = scaler.transform(df[['Price']])

    # Seed the forecast sequence with the last known window of prices
    sequence = prices[-look_back:].reshape(1, look_back, 1)
    predictions = []

    for _ in range(steps):
        # Predict the next scaled price
        pred = model.predict(sequence, verbose=0)
        predictions.append(pred[0, 0])

        # Slide the window forward: drop oldest value, append new prediction
        sequence = np.roll(sequence, -1, axis=1)
        sequence[0, -1, 0] = pred[0, 0]

    # Reverse the scaling to return predictions in original dollar values
    return scaler.inverse_transform(
        np.array(predictions).reshape(-1, 1)
    ).flatten()


def main():
    """
        Load stock data, train the LSTM model, and print future forecasts.
        
        Workflow:
        1. Load raw stock price data from CSV
        2. Scale prices and build sliding window sequences for LSTM input
        3. Construct the 2-layer LSTM neural network architecture
        4. Train the LSTM model on the prepared sequences
        5. Generate price predictions for the next 5 days
        6. Print each forecasted price in original dollar scale
    """
    df = pd.read_csv("data/stock_prices.csv")

    X, y, scaler = prepare_lstm_data(df)
    model = build_lstm()
    model = train_lstm(model, X, y)
    preds = forecast_lstm(model, df, scaler)

    print("\n=== LSTM Forecast (next 5 days) ===")
    for i, p in enumerate(preds, start=16):
        print(f"Day {i}: {p:.2f}")


# Program entry point
if __name__ == "__main__":
    main()
