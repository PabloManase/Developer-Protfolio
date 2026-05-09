
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


def load_data(path):
    return pd.read_csv(path)


def train_model(df):
    X = df[['YearsExperience']]
    y = df['Salary']

    model = LinearRegression()
    model.fit(X, y)

    return model, X, y


def evaluate_model(model, X, y):
    predictions = model.predict(X)

    mse = mean_squared_error(y, predictions)
    r2 = r2_score(y, predictions)

    return mse, r2


def predict_salary(model, years):
    return model.predict([[years]])[0]


def main():
    df = load_data("data/salary_data.csv")

    model, X, y = train_model(df)
    mse, r2 = evaluate_model(model, X, y)

    print("Model Evaluation:")
    print(f"MSE: {mse:.2f}")
    print(f"R² Score: {r2:.2f}")

    # Example prediction
    years = 5
    predicted_salary = predict_salary(model, years)

    print(f"\nPredicted salary for {years}"
          f"years experience: {predicted_salary:.2f}")


if __name__ == "__main__":
    main()
