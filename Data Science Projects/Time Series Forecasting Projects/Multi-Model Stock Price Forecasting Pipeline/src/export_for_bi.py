# --------------------------------------------------------------------------------
# BI Export Module
# Exports enriched historical data and forecast results as CSVs
# for use in Power BI and Tableau dashboards.
# --------------------------------------------------------------------------------

import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(__file__))
from forecast_model import (  # noqa: E402
    load_data,
    train_model,
    add_rolling_stats,
)


def export_dashboard_data():
    """
        Export processed data and forecasts as CSVs for Power BI
        
        Workflow:
        1. Load raw stock price data from CSV
        2. Compute rolling statistics and enrich the dataset
        3. Export enriched historical data to historical_enriched.csv
        4. Train Linear Regression model on the enriched data
        5. Generate future day indices for the next 10 days
        6. Predict prices for each future day
        7. Build a structured forecast DataFrame with model label
        8. Export forecast results to forecast_output.csv

        Processed files:
            data/historical_enriched.csv - historical prices with rolling stats
            data/forecast_output.csv     - predicted future prices
    """

    # Load raw stock data and process with rolling statistics
    df = load_data()
    df = add_rolling_stats(df)

    # Export processed historical data for use as a data source in BI tool
    df.to_csv("data/historical_enriched.csv", index=False)
    print("Saved: data/historical_enriched.csv")

    # Train Linear Regression model on copy to avoid mutating original
    model = train_model(df.copy())
    # Generate future day indices for the next 10 days beyond the dataset
    future_days_list = [[len(df) + i] for i in range(1, 11)]
    # Predict prices for each future day
    preds = model.predict(future_days_list)

    # Build structured forecast DataFrame(day index, price, model label)
    forecast_df = pd.DataFrame({
        'Day': range(len(df) + 1, len(df) + 11),
        'Predicted_Price': preds,
        'Model': 'LinearRegression'
    })

    # Export forecast results for use as a second data source in BI tools
    forecast_df.to_csv("data/forecast_output.csv", index=False)
    print("Saved: data/forecast_output.csv")


# Program entry point
if __name__ == "__main__":
    export_dashboard_data()
