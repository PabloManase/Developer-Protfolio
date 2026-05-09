
# Salary Prediction Using Linear Regression

##   Project Overview
This project demonstrates how to build a simple machine learning model using Linear Regression in Python.

The goal of the project is to predict employee salaries based on years of experience and evaluate the performance of the model using industry-standard metrics.

---

#   Objectives
- Understand linear regression
- Train a machine learning model
- Make salary predictions
- Evaluate model performance
- Visualize regression results

---

#   Technologies Used
- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Jupyter Notebook

---

#   Project Structure

```plaintext
linear-regression-salary-prediction/
│
├── data/
│   └── salary_data.csv
│
├── notebooks/
│   └── analysis.ipynb
│
├── src/
│   └── model.py
│
├── README.md
├── requirements.txt
```

---

#   Dataset

The dataset contains:
- Years of experience
- Corresponding salaries

Example:

| YearsExperience | Salary |
|----------------|--------|
| 1 | 30000 |
| 2 | 35000 |
| 3 | 40000 |

---

#   How the Project Works

## Step 1 — Load Data
The dataset is loaded using Pandas.

## Step 2 — Prepare Features
- `YearsExperience` is used as the input feature
- `Salary` is used as the target variable

## Step 3 — Train Model
A Linear Regression model is trained using Scikit-learn.

## Step 4 — Make Predictions
The model predicts salaries based on experience.

## Step 5 — Evaluate Performance
The following metrics are used:
- Mean Squared Error (MSE)
- R² Score

## Step 6 — Visualize Results
A regression line is plotted against the dataset.

---

#   Model Evaluation

The project evaluates:
- Prediction accuracy
- Relationship between variables
- Overall model performance

---

#   Visualization

The notebook generates:
- Scatter plot of actual data
- Regression line visualization

---

#   How to Run the Project

## 1. Clone the repository

```bash
git clone <your-github-repo-link>
```

## 2. Navigate into the project

```bash
cd linear-regression-salary-prediction
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Run the notebook

```bash
jupyter notebook
```

Open:

```plaintext
notebooks/analysis.ipynb
```

---

#   Business Value

This project demonstrates how machine learning can support:
- Salary forecasting
- HR analytics
- Budget planning
- Predictive decision-making

---

#   Future Improvements
- Add larger datasets
- Include more salary factors
- Use multiple linear regression
- Deploy as a web application

---

#   Author

Paballo Manase
