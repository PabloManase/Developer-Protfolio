import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder


# GLOBALS
le_gender = LabelEncoder()
le_education = LabelEncoder()
le_job_title = LabelEncoder()


def load_data(path):
    """
        Load and clean the salary dataset from a CSV file.

        Parameters:
            path : str
                File path to the CSV dataset.

        Returns:
            pandas.DataFrame
                Cleaned dataset ready for feature engineering.
    """

    df = pd.read_csv(path, encoding='utf-8-sig')

    # Drop rows where any column value is missing
    original_len = len(df)
    df = df.dropna()
    dropped_missing = original_len - len(df)

    # The next lowest salary in the dataset is R35,000.
    df = df[df['Salary'] >= 10000]
    dropped_outlier = original_len - dropped_missing - len(df)

    print("=" * 45)
    print(" DATA LOADING SUMMARY")
    print("=" * 45)
    print(f"  Total rows loaded     : {original_len}")
    print(f"  Rows dropped (NaN)    : {dropped_missing}")
    print(f"  Rows dropped (outlier): {dropped_outlier}")
    print(f"  Clean rows remaining  : {len(df)}")
    print(f"  Columns               : {list(df.columns)}")
    print("=" * 45)

    return df


# FEATURE ENGINEERING
def encode_features(df):
    """
        Convert categorical text columns into numeric values that the
        LinearRegression model can process.
        This function uses scikit-learn's LabelEncoder, which assigns each
        unique category a unique integer (alphabetical order).

        Parameters:
            df : pandas.DataFrame
                Cleaned dataset containing the raw categorical columns.

        Returns:
            df : pandas.DataFrame
                Dataset with three new encoded columns added:
                Gender_enc, Education_enc, JobTitle_enc.
    """
    # Encode Gender:  Female=0, Male=1
    df['Gender_enc'] = le_gender.fit_transform(df['Gender'])

    # Encode Education Level:  Bachelor's=0, Master's=1, PhD=2
    df['Education_enc'] = le_education.fit_transform(df['Education Level'])

    # Encode Job Title:  one integer per unique title (174 titles total)
    df['JobTitle_enc'] = le_job_title.fit_transform(df['Job Title'])

    print("\n  Encoding complete:")
    print(f"    Gender classes    : {list(le_gender.classes_)}")
    print(f"    Education classes : {list(le_education.classes_)}")
    print(
        f"    Job title count   : "
        f"{len(le_job_title.classes_)} unique titles"
    )

    return df


def prepare_features(df):
    """
        Separate the dataset into input features (X) and target variable (y).

        Parameters:
            df : pandas.DataFrame
                Dataset with encoded feature columns already added.

        Returns:
            X : pandas.DataFrame
                Input features matrix.
            y : pandas.Series
                Target salary values.
    """
    
    feature_columns = [
        'Age',
        'Gender_enc',
        'Education_enc',
        'JobTitle_enc',
        'Years of Experience'
    ]

    X = df[feature_columns]
    y = df['Salary']

    print(f"\n  Features : {feature_columns}")
    print("  Target   : Salary")

    return X, y


def split_data(X, y, test_size=0.2, random_state=42):
    """
        Split data into training (80%) and testing (20%) sets.

        Parameters:
            X            : pandas.DataFrame   Input features.
            y            : pandas.Series      Target salaries.
            test_size    : float              Fraction held out for testing.
            random_state : int                Seed for reproducibility.

        Returns:
            X_train, X_test, y_train, y_test
    """
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state
    )

    print(
        f"\n  Training samples : {len(X_train)}"
        f"  ({100 - test_size * 100:.0f}%)"
    )
    print(
        f"  Testing  samples : {len(X_test)}"
        f"   ({test_size * 100:.0f}%)"
    )

    return X_train, X_test, y_train, y_test


def train_model(X_train, y_train):
    """
        Train a Multiple Linear Regression model on the training data.

        Parameters:
            X_train : pandas.DataFrame   Training input features.
            y_train : pandas.Series      Training salary values.

        Returns:
            model : LinearRegression     Trained model object.
    """
    
    model = LinearRegression()
    model.fit(X_train, y_train)

    print("\n" + "=" * 45)
    print(" MODEL COEFFICIENTS")
    print("=" * 45)
    print(f"  Base salary (intercept) : ${model.intercept_:,.2f}")
    for feature, coef in zip(X_train.columns, model.coef_):
        direction = "▲" if coef >= 0 else "▼"
        print(f"  {feature:<25}: {direction} ${abs(coef):,.2f} per unit")
    print("=" * 45)

    return model


def evaluate_model(model, X_test, y_test):
    """
        Evaluate the trained model on unseen test data.

        Metrics explained:
            MSE   – Mean Squared Error. Average of (actual − predicted)².

            RMSE  – Root Mean Squared Error = √MSE.

            R²    – Coefficient of determination. Ranges from 0.0 to 1.0.

        Parameters:
            model  : LinearRegression
                Trained model.

            X_test : pandas.DataFrame
                Test input features.

            y_test : pandas.Series
                Actual test salaries.

        Returns:
            mse, rmse, r2 : float
    """
    
    predictions = model.predict(X_test)

    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, predictions)

    print("\n" + "=" * 45)
    print(" MODEL EVALUATION RESULTS")
    print("=" * 45)
    print(f"  Mean Squared Error (MSE) : ${mse:>15,.2f}")
    print(f"  Root MSE        (RMSE)   : ${rmse:>15,.2f}")
    print(
        f"  R² Score                 : "
        f"{r2:.4f}  ({r2 * 100:.2f}% variance explained)"
    )
    print("=" * 45)

    return mse, rmse, r2


def predict_salary(
    model, age, gender, education_level, job_title, years_experience
):
    """
        Predict salary for a single employee.

        Parameters:
            model              : LinearRegression
            age                : float
            gender             : str
            education_level    : str
            job_title          : str
            years_experience   : float

        Returns:
            float   Predicted annual salary in USD.
    """
    
    # Encode the string inputs to integers using the fitted encoders
    gender_enc = le_gender.transform([gender])[0]
    education_enc = le_education.transform([education_level])[0]
    job_title_enc = le_job_title.transform([job_title])[0]

    # Build a single-row DataFrame - column order must match training
    input_df = pd.DataFrame([[
        age,
        gender_enc,
        education_enc,
        job_title_enc,
        years_experience
    ]], columns=[
        'Age',
        'Gender_enc',
        'Education_enc',
        'JobTitle_enc',
        'Years of Experience'
    ])

    predicted = model.predict(input_df)[0]

    return round(predicted, 2)


def plot_actual_vs_predicted(
    model, X_test, y_test,
    save_path='visuals/prediction_plot.png'
):
    """
        Generate an Actual vs Predicted salary scatter plot and save it to disk.

        Parameters:
            model     : LinearRegression   Trained model.
            X_test    : pandas.DataFrame   Test features.
            y_test    : pandas.Series      Actual test salaries.
            save_path : str                Output file path.
    """
    predictions = model.predict(X_test)

    plt.figure(figsize=(10, 7))

    # Scatter: actual salary (x-axis) vs predicted salary (y-axis)
    plt.scatter(
        y_test, predictions,
        color='steelblue', alpha=0.65, edgecolors='white',
        linewidths=0.5, s=70, label='Predictions'
    )

    # Perfect prediction reference line
    min_val = min(y_test.min(), predictions.min())
    max_val = max(y_test.max(), predictions.max())
    plt.plot(
        [min_val, max_val], [min_val, max_val],
        'r--', linewidth=2, label='Perfect Prediction Line'
    )

    plt.xlabel('Actual Salary ($)', fontsize=13)
    plt.ylabel('Predicted Salary ($)', fontsize=13)
    plt.title(
        'Multiple Linear Regression - Actual vs Predicted Salary\n'
        'Features: Age, Gender, Education, Job Title, Years of Experience',
        fontsize=13
    )
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()

    print(f"\n  Plot saved -> {save_path}")


def main():
    """
        Full ML pipeline — run this file directly to train and evaluate the model.
        
        Workflow:
            1) Load and clean the dataset
            2) Encode categorical columns
            3) Separate features and target
            4) Split into training and testing sets
            5) Train the Multiple Linear Regression model
            6) Evaluate performance on the test set
            7) Example prediction
            8) Generate visualisation
    """

    df = load_data('data/salary_data.csv')    
    df = encode_features(df)   
    X, y = prepare_features(df)   
    X_train, X_test, y_train, y_test = split_data(X, y)    
    model = train_model(X_train, y_train)    
    mse, rmse, r2 = evaluate_model(model, X_test, y_test)
    
    print("\n" + "=" * 45)
    print(" EXAMPLE SALARY PREDICTION")
    print("=" * 45)

    example = {
        'age': 32,
        'gender': 'Male',
        'education_level': "Bachelor's",
        'job_title': 'Software Engineer',
        'years_experience': 5
    }

    predicted = predict_salary(model, **example)
    for key, val in example.items():
        print(f"  {key:<20}: {val}")
    print(f"  {'Predicted Salary':<20}: ${predicted:,.2f}")
    print("=" * 45)
    plot_actual_vs_predicted(model, X_test, y_test)


# Program Entry Point
if __name__ == "__main__":
    main()
