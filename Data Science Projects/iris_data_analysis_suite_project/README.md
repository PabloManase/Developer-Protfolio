# Iris Dataset — Exploratory Data Analysis (EDA)

## Project Overview

This project performs a comprehensive exploratory data analysis (EDA)
on the Iris flower dataset using Python. The analysis covers dataset
inspection, statistical summaries, data quality checks, professional
visualizations, interactive dashboards, machine learning classification
models, and a Power BI business intelligence report.

The project was developed as part of a Data Science technical assessment
focused on data exploration, visualization, and applied machine learning.

---

## Project Structure

```plaintext
Basic EDA Project/
│
├── data/
│   ├── iris_dataset.csv              # Original dataset (150 rows)
│
├── notebook/
│   └── analysis.ipynb                # Main Jupyter Notebook
│
├── visuals/
│   ├── histogram.png
│   ├── scatterplot.png
│   ├── species_distribution.png
│   ├── correlation_heatmap.png
│   ├── seaborn_pairplot.png
│   ├── seaborn_violin.png
│   ├── seaborn_boxplot.png 
│   ├── seaborn_heatmap.png
│   └── feature_importance.png
│
├── dashboard/
│   └── iris_eda_report.pbix          # Power BI Desktop report
│
├── dashboard.py                      # Plotly Dash interactive dashboard
├── prepare_for_powerbi.py            # Data cleaning script for Power BI
├── requirements.txt
└── README.md
```

---

## Dataset Information

The Iris dataset is one of the most widely used benchmark datasets in
data science and machine learning. It contains measurements of Iris
flowers across three species.

| Feature | Unit | Description |
|---|---|---|
| sepal_length | cm | Length of the flower sepal |
| sepal_width | cm | Width of the flower sepal |
| petal_length | cm | Length of the flower petal |
| petal_width | cm | Width of the flower petal |
| species | — | Flower species classification |

**Species:** Setosa · Versicolor · Virginica
**Rows:** 150 (50 per species) · **Columns:** 5 · **Missing values:** 0

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.12 | Core programming language |
| Pandas | Data loading, cleaning, and manipulation |
| NumPy | Numerical computations |
| Matplotlib | Base visualizations |
| Seaborn | Statistical visualizations |
| Scikit-learn | Machine learning classification models |
| Plotly | Interactive chart rendering |
| Dash | Interactive web dashboard framework |
| Power BI Desktop | Business intelligence report |
| Jupyter Notebook | Analysis environment |

---

## Analysis Performed

### Dataset Exploration
- Shape analysis, column inspection, data type verification
- Missing value analysis and duplicate detection

### Statistical Analysis
- Descriptive statistics: mean, min, max, quartiles, standard deviation
- Per-species statistical breakdowns

### Visualizations — Matplotlib
- Histogram of sepal length distribution
- Scatter plot of sepal length vs petal length
- Species distribution bar chart

### Visualizations — Seaborn
- Pair plot (all feature combinations, colour-coded by species)
- Violin plot (petal length distribution per species)
- Box plot with overlaid data points (sepal width per species)
- Correlation heatmap

### Correlation Analysis
- Full feature correlation matrix
- Matplotlib and Seaborn heatmaps with annotated coefficients

### Machine Learning Classification
Three models trained and evaluated on an 80/20 train-test split:

| Model | Description |
|---|---|
| Logistic Regression | Linear baseline classifier |
| Decision Tree | Rule-based interpretable model |
| Random Forest | Ensemble model (100 estimators) |

Outputs include accuracy comparison, classification report
(precision, recall, F1-score per species), feature importance
chart, and live prediction on unseen flower measurements.

### Interactive Dashboard (Plotly Dash)
- Dropdown-controlled scatter plot (any X vs Y feature combination)
- Dropdown-controlled box plot per species
- Species distribution bar chart
- All charts update dynamically without page reload

### Power BI Report
- Species distribution bar chart
- Scatter plot with species legend
- Slicer (filter control by species)
- Data table with average measurements
- Exported as `iris_eda_report.pbix`

---

## Key Insights

- Petal length and petal width are strongly positively correlated
  (r ≈ 0.96) — the most predictive feature pair in the dataset.
- Setosa flowers are linearly separable from the other two species
  based on petal measurements alone.
- Versicolor and Virginica show some overlap in sepal measurements
  but are distinguishable via petal dimensions.
- The Random Forest classifier achieves the highest accuracy on the
  test set among the three models evaluated.
- No missing values were detected in the original dataset.

---

## How to Run the Project

### Step 1 — Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_LINK
cd "Basic EDA Project"
```

### Step 2 — Install Required Libraries

```bash
pip install -r requirements.txt
```

### Step 3 — Run the Jupyter Notebook

```bash
jupyter notebook
```

Open `notebook/analysis.ipynb` and run all cells from top to bottom.
Always run the setup cell (Cell 1) first — it loads the dataset and
imports all libraries required by subsequent cells.

### Step 4 — Run the Interactive Dashboard

```bash
python dashboard.py
```

Open your browser and navigate to `http://127.0.0.1:8050`.
Press `Ctrl + C` in the terminal to stop the dashboard.


### Step 5 — Open the Power BI Report

Open `dashboard/iris_eda_report.pbix` in Power BI Desktop.

---

## Visualizations Generated

| File | Description |
|---|---|
| `histogram.png` | Sepal length frequency distribution |
| `scatterplot.png` | Sepal length vs petal length |
| `species_distribution.png` | Count of flowers per species |
| `correlation_heatmap.png` | Matplotlib feature correlation heatmap |
| `seaborn_pairplot.png` | All feature pair scatter plots |
| `seaborn_violin.png` | Petal length distribution by species |
| `seaborn_boxplot.png` | Sepal width quartiles by species |
| `seaborn_heatmap.png` | Seaborn feature correlation heatmap |
| `feature_importance.png` | Random Forest feature importance scores |

All visuals are saved to the `visuals/` folder automatically when
the notebook cells are executed.

---

## Skills Demonstrated

- Exploratory Data Analysis (EDA)
- Statistical Analysis and Interpretation
- Data Cleaning and Preparation
- Data Visualization (Matplotlib and Seaborn)
- Interactive Dashboard Development (Plotly Dash)
- Machine Learning Classification (Scikit-learn)
- Business Intelligence Reporting (Power BI)
- Python Programming
- Jupyter Notebook Workflow

---

## Author

**Paballo Manase**
Aspiring Software Engineer and Data Analyst

---

## License

This project is intended for educational and portfolio purposes.
