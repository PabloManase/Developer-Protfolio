# Data Dictionary — salary_data.csv

## Dataset Overview

| Property       | Value                          |
|----------------|--------------------------------|
| Source         | Kaggle — Salary Dataset        |
| Total rows     | 375 (372 after cleaning)       |
| Total columns  | 6                              |
| Target column  | Salary                         |

---

## Column Definitions

| Column               | Type    | Values / Range                                    | Notes                                                      |
|----------------------|---------|---------------------------------------------------|------------------------------------------------------------|
| Age                  | float   | 23 – 53                                           | Employee age in years                                      |
| Gender               | string  | Male, Female                                      | Encoded: Female=0, Male=1                                  |
| Education Level      | string  | Bachelor's, Master's, PhD                         | Encoded: Bachelor's=0, Master's=1, PhD=2                   |
| Job Title            | string  | 174 unique titles                                 | Encoded: alphabetical integer (0–173)                      |
| Years of Experience  | float   | 0 – 25                                            | Professional work experience in years                      |
| Salary               | float   | $35,000 – $250,000 (after cleaning)               | Annual salary in USD — this is the prediction target       |

---

## Data Cleaning Applied

1. **Removed 2 rows** containing NaN (missing) values across any column.
2. **Removed 1 row** where Salary = $350 — a clear data entry error.
   The next lowest salary in the dataset is $35,000.
3. Final clean dataset: **372 rows**.

---

## Train / Test Split

| Split    | Rows | Percentage |
|----------|------|------------|
| Training | 297  | 80%        |
| Testing  | 75   | 20%        |
