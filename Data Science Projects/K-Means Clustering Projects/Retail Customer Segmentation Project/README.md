# Customer Segmentation Using K-Means Clustering

A machine learning project that applies K-Means clustering to customer spending data to identify distinct
customer segments and uncover actionable behavioural patterns. Built with Python, Scikit-learn, Plotly, and
Dash - extended with an interactive web dashboard, Power BI integration, advanced algorithm benchmarking,
cluster performance evaluation, and dimensionality reduction using PCA.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Business Problem](#business-problem)
- [Project Objectives](#project-objectives)
- [Project Structure](#project-structure)
- [Dataset](#dataset)
- [Technologies and Libraries](#technologies-and-libraries)
- [Project Workflow](#project-workflow)
- [Cluster Performance Evaluation](#cluster-performance-evaluation)
- [Algorithm Comparison](#algorithm-comparison)
- [Key Insights](#key-insights)
- [Business Recommendations](#business-recommendations)
- [Visualisations](#visualisations)
- [Interactive Dashboard](#interactive-dashboard)
- [Power BI Integration](#power-bi-integration)
- [Skills Demonstrated](#skills-demonstrated)
- [How to Run](#how-to-run)
- [Author](#author)

---

## Project Overview

This project implements a complete unsupervised machine learning pipeline to segment customers based on their annual income and spending behaviour. The analysis progresses from basic exploratory data analysis through to advanced algorithm benchmarking, quantitative cluster evaluation, and interactive business intelligence dashboards.

The project is structured across two notebooks:

| Notebook | Purpose |
|---|---|
| `notebook/analysis.ipynb` | Baseline EDA, K-Means clustering, elbow method, and cluster visualisation |
| `notebook/advanced_analysis.ipynb` | Algorithm comparison, cluster performance metrics, and PCA dimensionality reduction |

---

## Business Problem

Businesses generate significant volumes of customer data but frequently lack the tools to identify meaningful customer groups within that data. Without segmentation, marketing and sales efforts are applied uniformly across an entire customer base — resulting in wasted budget, missed revenue opportunities, and poor customer experience.

This project solves that problem by using machine learning to automatically group customers by shared characteristics, enabling targeted strategies for each segment.

---

## Project Objectives

- Implement and evaluate the K-Means clustering algorithm on real customer data
- Apply the Elbow Method to determine the optimal number of clusters
- Quantify cluster quality using three independent evaluation metrics
- Compare K-Means against Agglomerative Clustering and Gaussian Mixture Models
- Reduce dimensionality using PCA and visualise clusters in principal component space
- Build a live interactive web dashboard that updates cluster charts dynamically
- Integrate results with Power BI for business reporting

---

## Project Structure

```
K-Means Clustering Project/
│
├── data/
│   ├── customer_data.csv                  # Original dataset (40 customers)
│   ├── customer_clusters_powerbi.csv      # Enriched export for Power BI
│   └── cluster_evaluation.csv             # Metric scores for K=2 to K=10
│
├── notebook/
│   ├── analysis.ipynb                     # Baseline analysis
│   └── advanced_analysis.ipynb            # Advanced evaluation and PCA
│
├── src/
│   └── app.py                             # Interactive Dash dashboard
│
├── dashboard/
│   └── CustomerSegmentation.pbix          # Power BI report file
│
├── visuals/
│   ├── clusters.png                       # K-Means cluster scatter plot
│   ├── elbow_method.png                   # Elbow method chart
│   ├── feature_distribution.png           # Income and score distributions
│   ├── cluster_evaluation.png             # Evaluation metrics across K values
│   ├── algorithm_comparison.png           # Side-by-side algorithm comparison
│   ├── pca_analysis.png                   # PCA scree plot and biplot
│   └── pca_clusters.png                   # Clusters visualised in PCA space
│
├── requirements.txt
└── README.md
```

---

## Dataset

| Column | Type | Description |
|---|---|---|
| `CustomerID` | Integer | Unique identifier per customer |
| `AnnualIncome` | Integer | Annual income in thousands |
| `SpendingScore` | Integer | Business-assigned score based on spending behaviour (0–100) |

- **Total records:** 40 customers
- **Income range:** 15 to 37 (thousands)
- **Spending Score range:** 3 to 99
- **Missing values:** None
- **Features used for clustering:** `AnnualIncome` and `SpendingScore`

---

## Technologies and Libraries

| Library | Version | Purpose |
|---|---|---|
| Python | 3.x | Core programming language |
| pandas | latest | Data loading, manipulation, and export |
| matplotlib | latest | Static chart generation |
| scikit-learn | latest | KMeans, Agglomerative, GMM, PCA, StandardScaler, evaluation metrics |
| plotly | latest | Interactive chart rendering |
| dash | latest | Web dashboard framework |
| dash-bootstrap-components | latest | Bootstrap layout system for the dashboard |
| jupyter | latest | Interactive notebook environment |

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

## Project Workflow

### 1. Data Loading and Exploration
The customer CSV is loaded into a pandas DataFrame. Initial exploration covers shape, data types, summary statistics, and missing value checks.

### 2. Feature Distribution Analysis
Histograms and descriptive statistics reveal that annual income is concentrated in the 15–37k range, while spending scores are broadly distributed from near zero to 99 — indicating meaningful variation suitable for clustering.

### 3. Feature Scaling
`StandardScaler` is applied before clustering. This ensures that income and spending score contribute equally to distance calculations, rather than income dominating due to its larger numeric scale.

### 4. Elbow Method
K-Means inertia (sum of squared distances from each point to its cluster centre) is computed for K=1 to K=10. The resulting elbow chart shows a clear inflection point at K=5, identifying it as the optimal cluster count.

### 5. K-Means Clustering
K-Means is applied at K=5 with `random_state=42` for reproducibility and `n_init=10` to avoid poor local optima. Each customer is assigned to one of five clusters.

### 6. Cluster Visualisation
A scatter plot of Annual Income vs Spending Score, colour-coded by cluster, confirms that the five groups are visually distinct and interpretable in business terms.

### 7. Advanced Evaluation and Algorithm Comparison
Three quantitative metrics are computed across K=2 to K=10. K-Means is also benchmarked against two alternative algorithms at K=5. Full results are documented in the sections below.

### 8. Dimensionality Reduction with PCA
Principal Component Analysis is applied to the scaled feature space. A scree plot confirms that two principal components explain 100% of the variance in this two-feature dataset. Cluster membership is visualised in PCA space and a biplot shows feature loading directions.

---

## Cluster Performance Evaluation

Three independent metrics were computed for K=2 to K=10 to objectively identify the optimal number of clusters:

| K | Silhouette ↑ | Davies-Bouldin ↓ | Calinski-Harabasz ↑ |
|---|---|---|---|
| 2 | 0.4138 | 1.0155 | 29.64 |
| 3 | 0.4092 | 0.7784 | 33.58 |
| **4** | **0.4558** | 0.6855 | 48.99 |
| 5 | 0.4479 | 0.7118 | 48.38 |
| 6 | 0.4312 | 0.7119 | 52.93 |
| 7 | 0.4503 | **0.6342** | 54.06 |
| 8 | 0.4313 | 0.7104 | 55.33 |
| **9** | 0.4277 | 0.7112 | **56.55** |
| 10 | 0.4170 | 0.6780 | 54.73 |

**Metric definitions:**
- **Silhouette Score** — measures how similar each point is to its own cluster versus neighbouring clusters. Range: −1 to +1. Higher is better.
- **Davies-Bouldin Index** — measures average cluster similarity to the nearest cluster. Range: 0 to ∞. Lower is better.
- **Calinski-Harabasz Score** — ratio of between-cluster to within-cluster dispersion. Range: 0 to ∞. Higher is better.

**Finding:** The three metrics individually favour different values of K (4, 7, and 9 respectively). The scores at K=4 and K=5 are close across all three metrics. K=5 — the value selected by the Elbow Method — represents a well-supported balance across all measures and is retained for the final analysis.

---

## Algorithm Comparison

K-Means was benchmarked against Agglomerative Clustering and the Gaussian Mixture Model at K=5:

| Algorithm | Silhouette ↑ | Davies-Bouldin ↓ | Calinski-Harabasz ↑ |
|---|---|---|---|
| **K-Means** | **0.4479** | 0.7118 | **48.38** |
| Agglomerative | 0.4290 | 0.7233 | 44.12 |
| Gaussian Mixture | 0.3875 | **0.7012** | 35.73 |

**Finding:** K-Means outperforms both alternatives on Silhouette Score and Calinski-Harabasz. The Gaussian Mixture Model records a marginally lower Davies-Bouldin score but produces substantially weaker Silhouette results (0.3875 vs 0.4479), indicating less clearly defined cluster boundaries. The choice of K-Means in the baseline analysis is confirmed as the strongest algorithm for this dataset.

---

## Key Insights

At K=5, the clustering identified five distinct customer segments:

| Cluster | Avg Income (k) | Avg Spending Score | Customers | Segment Profile |
|---|---|---|---|---|
| 0 | 20.0 | 81.1 | 11 | Low income, very high spenders |
| 1 | 26.0 | 25.9 | 7 | Moderate income, low spenders |
| 2 | 18.5 | 17.0 | 8 | Low income, low spenders |
| 3 | 30.8 | 77.4 | 9 | Higher income, high spenders |
| 4 | 33.4 | 13.0 | 5 | Highest income, lowest spenders |

**Cluster 0 — Low Income, High Spend (11 customers):** Spending significantly exceeds what their income level would predict. These customers are emotionally or habitually driven buyers and are highly responsive to loyalty programmes and exclusive offers.

**Cluster 1 — Moderate Income, Low Spend (7 customers):** Financial capacity exists but is not being activated. The highest-opportunity group for conversion — targeted promotions or trust-building campaigns could unlock significant spend.

**Cluster 2 — Low Income, Low Spend (8 customers):** Budget-constrained customers. Price-sensitive messaging, value-focused offers, and discounts are the most appropriate strategy.

**Cluster 3 — Higher Income, High Spend (9 customers):** Consistently valuable customers. Retention strategies — personalised recommendations, early access, and loyalty rewards — are well-justified for this segment.

**Cluster 4 — Highest Income, Lowest Spend (5 customers):** The most financially capable but least engaged segment. Understanding the root cause of their low engagement — brand perception, product fit, or communication — is the key strategic challenge for this group.

---

## Business Recommendations

1. **Retain K=5 for operational use.** The evaluation metrics confirm this is a defensible, data-supported choice — not an arbitrary visual selection.

2. **Prioritise Clusters 1 and 4 for conversion campaigns.** Both segments have financial capacity that is not reflected in their current spending. Re-engagement campaigns targeting these groups have the highest potential return on marketing investment.

3. **Protect Cluster 3 with retention investment.** These are reliable mid-to-high value customers. Churn from this segment would have a disproportionate revenue impact.

4. **Apply value messaging to Cluster 2.** Budget-conscious customers respond to demonstrable value, not aspirational messaging. Adjust communication strategy accordingly.

5. **Test K=4 for simpler campaign structures.** The Silhouette Score is marginally higher at K=4 (0.4558 vs 0.4479). If operational simplicity is a priority, four segments may be easier to act on without meaningfully sacrificing cluster quality.

---

## Visualisations

All charts are saved in the `visuals/` folder and generated automatically when the notebooks are run.

| File | Description |
|---|---|
| `clusters.png` | Scatter plot of customer clusters at K=5 |
| `elbow_method.png` | Inertia vs K chart used to select optimal cluster count |
| `feature_distribution.png` | Histogram of income and spending score distributions |
| `cluster_evaluation.png` | Line charts of Silhouette, Davies-Bouldin, and Calinski-Harabasz across K values |
| `algorithm_comparison.png` | Side-by-side scatter plots for K-Means, Agglomerative, and GMM |
| `pca_analysis.png` | Scree plot and biplot showing principal component structure |
| `pca_clusters.png` | K-Means cluster assignments visualised in PCA space |

---

## Interactive Dashboard

The project includes a fully interactive web dashboard built with Plotly and Dash.

**Location:** `src/app.py`

**Features:**
- Cluster count slider (K=2 to K=10) — all four charts update instantly when adjusted
- Scatter plot — each dot is a customer, coloured by cluster, with CustomerID tooltip on hover
- Bar chart — number of customers per cluster
- Elbow method chart — with a dynamic vertical marker at the currently selected K
- Income distribution histogram — broken down by cluster colour

**To run the dashboard:**

```bash
cd src
python app.py
```

Then open `http://127.0.0.1:8050` in your browser.

---

## Power BI Integration

Cluster results are exported to `data/customer_clusters_powerbi.csv`, which includes segment labels and cluster centroid coordinates alongside the original customer data. This file is ready to import directly into Power BI Desktop.

**Power BI report file:** `dashboard/CustomerSegmentation.pbix`

The report contains a cluster scatter chart, segment size donut chart, average income by segment bar chart, and a summary statistics table, all connected to a segment slicer for interactive filtering.

---

## Skills Demonstrated

**Machine Learning**
- Unsupervised learning with K-Means clustering
- Algorithm benchmarking (K-Means vs Agglomerative vs Gaussian Mixture Model)
- Cluster quality evaluation using Silhouette Score, Davies-Bouldin Index, and Calinski-Harabasz Score
- Dimensionality reduction with PCA
- Feature scaling with StandardScaler
- Elbow Method for optimal K selection

**Data Analysis and Engineering**
- Exploratory data analysis with pandas
- Feature engineering and cluster profiling
- CSV export pipelines for BI tool integration

**Data Visualisation**
- Static charts with Matplotlib
- Interactive charts with Plotly
- Live web dashboard with Dash and Bootstrap layout
- Business intelligence reporting in Power BI

**Software Engineering**
- Modular, well-commented code
- Reproducible analysis with fixed random seeds
- Clean project structure with separation of notebooks, source code, data, and visuals

---

## How to Run

### Step 1 — Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_LINK
cd kmeans-clustering-project
```

### Step 2 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Run the Baseline Analysis

```bash
jupyter notebook
```

Open `notebook/analysis.ipynb` and run all cells sequentially.

### Step 4 — Run the Advanced Analysis

Open `notebook/advanced_analysis.ipynb` and run all cells sequentially.

This generates `data/cluster_evaluation.csv` and all advanced visualisations in the `visuals/` folder.

### Step 5 — Launch the Interactive Dashboard

```bash
cd src
python app.py
```

Open `http://127.0.0.1:8050` in your browser.

### Step 6 — Open the Power BI Report *(optional)*

Open `dashboard/CustomerSegmentation.pbix` in Power BI Desktop. If prompted, repoint the data source to `data/customer_clusters_powerbi.csv`.

---

## Author

**Paballo Manase**  
Aspiring Software Engineer | Data Analyst | Machine Learning Enthusiast

---

## License

This project was created for educational, portfolio, and technical assessment purposes.
