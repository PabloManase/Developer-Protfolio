# Salary Predictor — Multiple Linear Regression

A Python-based salary prediction system that analyses real-world employee
records and predicts annual salary based on five personal and professional
attributes. The project includes a trained Multiple Linear Regression model,
categorical feature encoding, model evaluation metrics, and an interactive
Flask web application for browser-based predictions.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Dataset](#dataset)
- [ML Pipeline](#ml-pipeline)
- [Model Evaluation](#model-evaluation)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Flask Web Application](#flask-web-application)
- [Example Output](#example-output)
- [Future Improvements](#future-improvements)
- [Author](#author)

---

## Project Overview

This project demonstrates an end-to-end machine learning workflow built in
Python. Starting from a simple linear regression on a 10-row toy dataset,
the system was progressively improved across four stages to incorporate a
real-world dataset, multiple salary-influencing features, a Multiple Linear
Regression model, and full web deployment via Flask.

The project was developed as part of a data science portfolio to demonstrate
practical skills in:

- Data loading, cleaning, and preprocessing
- Categorical feature encoding with `LabelEncoder`
- Machine learning model development and evaluation
- Train-test splitting and model validation
- Data visualisation with Matplotlib
- Web application development with Flask and Bootstrap 5

---

## Technologies Used

| Category | Tools |
|---|---|
| Language | Python 3.12 |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Visualisation | Matplotlib |
| Web Framework | Flask |
| Frontend | Bootstrap 5, Bootstrap Icons |
| Notebook | Jupyter Notebook |

---

## Project Structure

```
Linear Regression Project/
│
├── data/
│   ├── salary_data.csv          <- real-world dataset (375 rows, 6 columns)
│   ├── data_dictionary.md       <- column definitions and cleaning notes
│   └── prediction_plot.png      <- actual vs predicted chart (auto-generated)
│
├── src/
│   └── model.py                 <- full ML pipeline
│
├── visuals/
│   └── prediction_plot.png      <- chart saved by model.py
│
├── web/
│   ├── app.py                   <- Flask web application
│   └── templates/
│       └── index.html           <- prediction form (Bootstrap 5)
│
├── notebook/
│   └── analysis.ipynb           <- exploratory data analysis
│
├── requirements.txt
└── README.md
```

---

## Dataset

**Source:** Kaggle — Salary Dataset  
**File:** `data/salary_data.csv`

| Column | Type | Values / Range | Description |
|---|---|---|---|
| Age | float | 23 – 53 | Employee age in years |
| Gender | string | Male, Female | Encoded: Female=0, Male=1 |
| Education Level | string | Bachelor's, Master's, PhD | Encoded: Bachelor's=0, Master's=1, PhD=2 |
| Job Title | string | 174 unique titles | Encoded: alphabetical integer (0–173) |
| Years of Experience | float | 0 – 25 | Professional work experience in years |
| Salary | float | $35,000 – $250,000 | Annual salary in USD — prediction target |

**Cleaning applied:**

| Step | Action | Rows Affected |
|---|---|---|
| 1 | Removed rows with missing values (NaN) | 2 rows dropped |
| 2 | Removed row where Salary = $350 (data entry error) | 1 row dropped |
| — | **Final clean dataset** | **372 rows** |

---

## ML Pipeline

The pipeline in `src/model.py` is broken into eight clearly separated,
documented functions:

| Step | Function | Responsibility |
|---|---|---|
| 1 | `load_data()` | Reads CSV with UTF-8 BOM encoding, drops NaN rows, removes the $350 outlier |
| 2 | `encode_features()` | Converts Gender, Education Level, and Job Title to integers using `LabelEncoder` |
| 3 | `prepare_features()` | Splits the DataFrame into `X` (5 input features) and `y` (Salary target) |
| 4 | `split_data()` | 80/20 train-test split with `random_state=42` for reproducibility |
| 5 | `train_model()` | Fits `LinearRegression` on the training set; prints coefficients per feature |
| 6 | `evaluate_model()` | Calculates MSE, RMSE, and R² on the held-out test set |
| 7 | `predict_salary()` | Encodes a new single-row input and returns a predicted salary |
| 8 | `plot_actual_vs_predicted()` | Saves an Actual vs Predicted scatter plot to `visuals/` |

### Feature Encoding

Three columns contain text that `LinearRegression` cannot process directly.
`LabelEncoder` assigns each unique string a unique integer in alphabetical
order:

```
Gender          : Female=0, Male=1
Education Level : Bachelor's=0, Master's=1, PhD=2
Job Title       : Account Manager=0, Accountant=1, ... (174 titles → 0–173)
```

The fitted encoders are module-level globals (`le_gender`, `le_education`,
`le_job_title`) so that `web/app.py` imports and reuses the exact same
mapping at prediction time without retraining.

### Train-Test Split

80% of the 372 clean rows (297 rows) are used to train the model. The
remaining 20% (75 rows) are held out as a test set. The model never sees
the test set during training — this gives a fair, unbiased measure of how
well the model generalises to new data.

---

## Model Evaluation

The model is evaluated on the 75-row held-out test set using three metrics:

| Metric | Value | Description |
|---|---|---|
| **MSE** | 218,988,862.08 | Mean Squared Error — average of (actual − predicted)² |
| **RMSE** | $14,798.27 | Root MSE — average prediction error in dollar terms |
| **R²** | **0.9140** | 91.40% of salary variation explained by the model |

**Model coefficients (salary impact per one-unit increase):**

| Feature | Direction | Impact |
|---|---|---|
| Age | ▲ | +$3,419.52 per year |
| Gender | ▲ | +$8,169.92 (Male vs Female) |
| Education Level | ▲ | +$14,603.45 per level step |
| Job Title | ▲ | +$43.25 per encoded unit |
| Years of Experience | ▲ | +$2,164.47 per year |
| Intercept (base) | — | −$64,982.82 |

---

## Installation

### Step 1 — Clone or download the project

```bash
git clone <your-repo-url>
cd "Linear Regression Project"
```

### Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

**`requirements.txt`:**

```
pandas
numpy
matplotlib
scikit-learn
flask
jupyter
```

---

## How to Run

### Train and evaluate the model

Run the full ML pipeline from the project root:

```bash
python src/model.py
```

This loads and cleans the data, encodes features, trains the model, prints
evaluation metrics, runs an example prediction, and saves the Actual vs
Predicted chart to `visuals/prediction_plot.png`.

**Expected terminal output:**

```
=============================================
 DATA LOADING SUMMARY
=============================================
  Total rows loaded     : 375
  Rows dropped (NaN)    : 2
  Rows dropped (outlier): 1
  Clean rows remaining  : 372
=============================================

  Encoding complete:
    Gender classes    : ['Female', 'Male']
    Education classes : ["Bachelor's", "Master's", 'PhD']
    Job title count   : 174 unique titles

  Training samples : 297  (80%)
  Testing  samples : 75   (20%)

=============================================
 MODEL EVALUATION RESULTS
=============================================
  Mean Squared Error (MSE) : $  218,988,862.08
  Root MSE        (RMSE)   : $       14,798.27
  R² Score                 : 0.9140  (91.40% variance explained)
=============================================

=============================================
 EXAMPLE SALARY PREDICTION
=============================================
  age                 : 32
  gender              : Male
  education_level     : Bachelor's
  job_title           : Software Engineer
  years_experience    : 5
  Predicted Salary    : $70,310.70
=============================================

  Plot saved -> visuals/prediction_plot.png
```

### Launch Jupyter Notebook

```bash
jupyter notebook
```

Open `notebook/analysis.ipynb` for exploratory data analysis and
visualisations.

---

## Flask Web Application

The web app in `web/app.py` exposes two routes:

| Route | Method | Purpose |
|---|---|---|
| `/` | GET | Renders the prediction form with all dropdown options populated |
| `/predict` | POST | Receives form values, runs the model, returns the predicted salary |

### How it works

1. On startup, `app.py` trains the model and populates the dropdown lists
   from the fitted `LabelEncoder` objects.
2. The user fills in Age, Gender, Education Level, Job Title, and Years of
   Experience, then clicks **Predict Salary**.
3. Flask encodes the text inputs using the same encoders used during
   training, builds a single-row DataFrame, and calls `model.predict()`.
4. The predicted salary is displayed in a styled result box on the same page.
5. The form refills itself with the previous values after submission so the
   user can adjust one field and re-predict without re-entering everything.

**Input validation:**
- Age must be between 18 and 70
- Years of experience must be between 0 and 40
- Any `ValueError` is caught and shown in a styled error box — the server
  does not crash on invalid input

### Launch the web application

Run from the project root folder (not from inside `web/`):

```bash
python web/app.py
```

Open your browser and go to: **http://127.0.0.1:5000**

> **Important:** always run from the project root. The app resolves paths
> like `data/salary_data.csv` relative to the root, not to `web/`.

To stop the server: press `Ctrl + C` in the terminal.

---

## Example Output

**Model pipeline (terminal):**

```
  R² Score : 0.9140  (91.40% variance explained)
  RMSE     : $14,798.27

  Predicted Salary (Software Engineer, 5 yrs, Bachelor's, Male, Age 32):
  $70,310.70
```

**Web application:** the form accepts all five inputs via dropdowns and
number fields. After submission, a green result box displays the predicted
annual salary formatted as a currency string (e.g. `$70,310.70`). If a
field is invalid or out of range, a red error box appears instead.

---

## Future Improvements

- Deploy the Flask app to a live server (Render, Railway, or PythonAnywhere)
  for a publicly accessible URL
- Fetch live salary data via an external API to keep the dataset current
- Add cross-validation using `KFold` for more robust evaluation
- Try regularised models — Ridge or Lasso Regression — to reduce the impact
  of multicollinearity between Age and Years of Experience
- Build a prediction history table in the web UI showing the last N
  predictions made in the session
- Add a feature importance chart to the web app showing which factors most
  influence the predicted salary

---

## Author

**Paballo Manase**  
Aspiring Software Engineer and Data Analyst


