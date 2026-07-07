# Stock Price Time Series Forecasting

A Python-based time series forecasting system that analyses historical stock
prices and generates future price predictions using multiple machine learning
and statistical models. The project includes an interactive Streamlit
dashboard, anomaly detection, advanced feature engineering, model evaluation
metrics, and Power BI integration.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Dataset](#dataset)
- [Models Implemented](#models-implemented)
- [Features & Analysis](#features--analysis)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Streamlit Dashboard](#streamlit-dashboard)
- [Power BI Dashboard](#power-bi-dashboard)
- [Model Evaluation](#model-evaluation)
- [Example Output](#example-output)
- [Future Improvements](#future-improvements)
- [Author](#author)

---

## Project Overview

This project demonstrates an end-to-end time series forecasting workflow built
in Python. Starting from a simple linear regression baseline, the system has
been extended to incorporate multiple forecasting algorithms, rolling
statistical analysis, anomaly detection, advanced feature engineering, and
an interactive real-time dashboard.

The project was developed as part of a data analytics portfolio to demonstrate
practical skills in:

- Time series analysis and preprocessing
- Machine learning model development and evaluation
- Statistical forecasting with ARIMA
- Deep learning forecasting with LSTM neural networks
- Prophet-based decomposable forecasting
- Feature engineering and MinMax scaling
- Interactive dashboard development with Streamlit
- Business intelligence integration with Power BI

---

## Technologies Used

| Category | Tools |
|---|---|
| Language | Python 3.12 |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Statistical Forecasting | Statsmodels (ARIMA, Seasonal Decomposition) |
| Deep Learning | TensorFlow / Keras (LSTM) |
| Prophet Forecasting | Facebook Prophet |
| Visualization | Matplotlib, Plotly |
| Dashboard | Streamlit |
| Business Intelligence | Power BI |
| Notebook | Jupyter Notebook |

---

## Project Structure

```
Time Series Forecasting Project/
│
├── data/
│   ├── stock_prices.csv              # Raw historical stock price data
│   ├── historical_enriched.csv       # Enriched data exported for Power BI / Tableau
│   └── forecast_output.csv           # Forecast results exported for Power BI / Tableau
│
├── dashboard/
│   └── app.py                        # Streamlit interactive dashboard
│
├── notebook/
│   └── analysis.ipynb                # Jupyter Notebook — exploratory data analysis
│
├── src/
│   ├── forecast_model.py             # Core module: Linear Regression, ARIMA, evaluation
│   ├── prophet_model.py              # Facebook Prophet forecasting module
│   ├── lstm_model.py                 # LSTM neural network forecasting module
│   ├── anomaly_detection.py          # Z-score and IQR anomaly detection
│   ├── feature_engineering.py        # 16-feature engineering pipeline
│   └── export_for_bi.py              # CSV export script for Power BI and Tableau
│
├── visualization/
│   └── dashboard.pbix                # Power BI dashboard file
│
├── README.md
└── requirements.txt
```

---

## Dataset

The dataset (`data/stock_prices.csv`) contains daily historical stock price
records with the following structure:

| Column | Type | Description |
|---|---|---|
| `Date` | string | Trading date in `YYYY-MM-DD` format |
| `Price` | float | Daily closing stock price |

**Sample data:**

| Date | Price |
|---|---|
| 2024-01-01 | 100 |
| 2024-01-02 | 102 |
| 2024-01-03 | 101 |
| 2024-01-04 | 105 |
| 2024-01-05 | 107 |

> To extend the dataset with real market data, use the `yfinance` library:
>
> ```python
> import yfinance as yf
> df = yf.download('AAPL', start='2023-01-01', end='2024-01-01')
> ```

---

## Models Implemented

### 1. Linear Regression (Baseline)
Maps sequential day numbers to closing prices to establish a trend line.
Used as the performance baseline for comparison against more advanced models.
Includes an 80/20 train/test split with RMSE, MAE, and R² evaluation.

### 2. ARIMA
AutoRegressive Integrated Moving Average — a classical statistical model
configured with order `(2, 1, 2)` to capture autoregressive behaviour, trend
differencing, and moving average smoothing. Implemented via `statsmodels`.

### 3. Facebook Prophet
A decomposable forecasting model that separates price data into trend,
seasonality, and holiday components. Robust against missing data and outliers.
Outputs point forecasts alongside lower and upper confidence intervals
(`yhat`, `yhat_lower`, `yhat_upper`).

### 4. LSTM Neural Network
A Long Short-Term Memory recurrent neural network built in Keras. Uses a
sliding window of three previous closing prices (`look_back=3`) to predict
the next day's price. Architecture: two stacked LSTM layers (50 units each)
followed by a single Dense output neuron. Trained using the Adam optimizer
with Mean Squared Error loss.

---

## Features & Analysis

### Rolling Statistics (`add_rolling_stats`)
Computed dynamically for configurable window sizes (default: 3, 5, 7 days):

- Moving averages — MA_3, MA_5, MA_7
- Rolling standard deviation — measures short-term volatility
- Price momentum — 3-day directional change
- Daily percentage return

### Feature Engineering (`feature_engineering.py`)
A 16-feature pipeline providing diverse signals to downstream models:

| Category | Features |
|---|---|
| Trend | Day, MA_3, MA_5, MA_7, EMA_5 |
| Momentum | Return_1d, Return_3d, Price_vs_MA5 |
| Volatility | Rolling_Std_5, Price_Range_5 |
| Calendar | DayOfWeek, IsMonday, IsFriday |
| Lag | Lag_1, Lag_2, Lag_3 |

### Anomaly Detection (`anomaly_detection.py`)
Two detection methods implemented:

- **Z-score** — flags prices deviating more than 2 standard deviations from
  the mean; suitable for normally distributed price data
- **IQR** — flags prices outside 1.5x the interquartile range; more robust
  for skewed distributions

### Seasonal Decomposition (`analyze_trends`)
Decomposes the price series into three additive components using
`statsmodels.tsa.seasonal.seasonal_decompose` with a 5-day working week
period:

- **Trend** — underlying directional price movement
- **Seasonality** — repeating weekly price patterns
- **Residual** — unexplained noise after trend and seasonality are removed

---

## Installation

### Step 1 — Clone or download the project

```bash
git clone <your-repo-url>
cd "Time Series Forecasting Project"
```

### Step 2 — Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:** Prophet may take several minutes to install on Windows as it
> compiles Stan models internally. If installation fails, run
> `pip install pystan==2.19.1.1` first, then retry.

---

## How to Run

### Run the core forecasting pipeline

```bash
cd "Time Series Forecasting Project"
python src/forecast_model.py
```

Executes the full workflow: loads data, engineers features, trains Linear
Regression and ARIMA models, evaluates performance metrics, prints forecasts,
and saves a comparison chart to `forecast_chart.png`.

### Run Facebook Prophet forecasting

```bash
python src/prophet_model.py
```

### Run LSTM neural network forecasting

```bash
python src/lstm_model.py
```

### Run anomaly detection

```bash
python src/anomaly_detection.py
```

### Export data for Power BI or Tableau

```bash
python src/export_for_bi.py
```

Generates two files in the `data/` directory:

- `historical_enriched.csv` — historical prices with all rolling statistics
- `forecast_output.csv` — 10-day Linear Regression forecast with model labels

### Launch Jupyter Notebook

```bash
jupyter notebook
```

Open `notebook/analysis.ipynb` for exploratory data analysis and
inline visualisations.

---

## Streamlit Dashboard

The interactive dashboard provides real-time forecasting with adjustable
user controls.

### Launch the dashboard

```bash
streamlit run dashboard/app.py
```

Opens automatically at `http://localhost:8501`.

### Dashboard features

| Feature | Description |
|---|---|
| Summary metric cards | Latest price, daily return %, 5-day high, 5-day low |
| Interactive Plotly chart | Historical prices, moving average overlay, forecast line |
| Forecast days slider | Adjust forecast horizon from 3 to 30 days |
| Moving average toggle | Enable/disable MA overlay and select window size |
| Forecast table | Date-mapped predicted prices, sortable by column |

---

## Power BI Dashboard

A pre-built Power BI dashboard (`visualization/dashboard.pbix`) is included
for executive-level reporting.

### Connecting updated data

1. Run the export script to regenerate the CSV files:

   ```bash
   python src/export_for_bi.py
   ```

2. Open `visualization/dashboard.pbix` in Power BI Desktop.
3. Navigate to **Home > Transform Data > Data Source Settings**.
4. Update the file paths to point to `data/historical_enriched.csv` and
   `data/forecast_output.csv`.
5. Click **Refresh** to reload the latest data into the dashboard.

---

## Model Evaluation

All models are evaluated on a held-out test set representing 20% of the
data, split in time order with no shuffling to preserve the sequential
nature of the series.

| Metric | Description | Target |
|---|---|---|
| **RMSE** | Root Mean Squared Error — penalises large errors more heavily | Minimise |
| **MAE** | Mean Absolute Error — average dollar error per prediction | Minimise |
| **R²** | Coefficient of determination — proportion of variance explained | Closer to 1.0 |

**Example evaluation output:**

```
=== Model Evaluation ===
RMSE  : 1.2847  (avg error in $ terms, squared)
MAE   : 1.0312  (avg dollar error per prediction)
R2    : 0.9823  (1.0 = perfect, 0.0 = no better than mean)
```

---

## Example Output

```
Training on 12 rows, testing on 3 rows

=== Model Evaluation ===
RMSE  : 1.2847
MAE   : 1.0312
R2    : 0.9823

===================================
 Future Stock Price Forecast
===================================

Predicted Price for Day 16: 129.43
Predicted Price for Day 17: 131.21
Predicted Price for Day 18: 132.99
Predicted Price for Day 19: 134.77
Predicted Price for Day 20: 136.55

Forecasting Complete.

=== ARIMA Forecast ===
Day 16: 130.11
Day 17: 131.87
Day 18: 133.04
Day 19: 134.22
Day 20: 135.91

Chart saved to forecast_chart.png

=== Anomaly Detection Report ===
No anomalies detected in the dataset.
```

---

## Future Improvements

- Fetch live stock data via `yfinance` to replace the static CSV
- Implement `auto_arima` from `pmdarima` for automated ARIMA order selection
- Add `TimeSeriesSplit` cross-validation for more robust model evaluation
- Build a side-by-side model comparison table reporting RMSE and MAE
- Add a volatility heatmap calendar to the Streamlit dashboard
- Deploy the Streamlit dashboard to Streamlit Cloud
- Implement email or webhook alerts triggered by anomaly detection

---

## Author

**Paballo Manase**
Information Technology Student | Aspiring Software Engineer & Data Analyst

---

## License

This project is developed for educational and portfolio purposes.
