# --------------------------------------------------------------------------------
# Anomaly Detection Module
# Identifies unusual stock price movements using Z-score and IQR methods.
# --------------------------------------------------------------------------------

import pandas as pd


def detect_anomalies_zscore(df, threshold=2.0):
    """
        Flag data points that are unusually far from the mean.
        A Z-score above the threshold = anomaly.

        Parameters:
            df : pandas.DataFrame - stock data with 'Price' column
            threshold : float - Z-score cutoff (2.0 = top/bottom 5%)

        Returns:
            pandas.DataFrame - original df with 'Z_Score'
            and 'Is_Anomaly' columns
    """
    
    df = df.copy()

    # Calculate the mean and standard deviation of the price series
    mean = df['Price'].mean()
    std = df['Price'].std()

    # Z-score measures how many standard deviations each price is from the mean
    df['Z_Score'] = (df['Price'] - mean) / std

    # Flag any price whose absolute Z-score exceeds the threshold as an anomaly
    df['Is_Anomaly'] = df['Z_Score'].abs() > threshold

    return df


def detect_anomalies_iqr(df):
    """
        Alternative method: flag outliers using Interquartile Range.
        More robust than Z-score for skewed distributions.

        Returns:
            pandas.DataFrame - with 'Is_Outlier' boolean column
    """
    
    df = df.copy()

    # Calculate the 25th and 75th percentile boundaries
    Q1 = df['Price'].quantile(0.25)
    Q3 = df['Price'].quantile(0.75)
    IQR = Q3 - Q1

    # Prices beyond 1.5x IQR from Q1/Q3 are considered outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    df['Is_Outlier'] = (
        (df['Price'] < lower_bound) |
        (df['Price'] > upper_bound)
    )

    return df


def print_anomaly_report(df):
    """
        Print a formatted summary of all detected anomalies.
        Uses the Z-score method for detection.

        Parameters:
            df : pandas.DataFrame - raw stock price data
    """
    
    df = detect_anomalies_zscore(df)
    anomalies = df[df['Is_Anomaly']]

    print("\n=== Anomaly Detection Report ===")

    if anomalies.empty:
        print("No anomalies detected in the dataset.")
    else:
        print(f"Found {len(anomalies)} anomalous price point(s):\n")
        print(anomalies[['Date', 'Price', 'Z_Score']].to_string(index=False))


def main():
    """
        Load stock data and run the anomaly detection report.
        
        Workflow:
        1. Load raw stock price data from CSV
        2. Run the anomaly detection report and print results
    """
    
    df = pd.read_csv("data/stock_prices.csv")
    print_anomaly_report(df)


# Program entry point
if __name__ == "__main__":
    main()
