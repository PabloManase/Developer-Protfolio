import sys
import os

# Add the project root directory to Python's module search path.
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

from flask import Flask, render_template, request  # noqa: E402

from src.model import (  # noqa: E402
    load_data,
    encode_features,
    prepare_features,
    split_data,
    train_model,
    predict_salary,
    le_gender,
    le_education,
    le_job_title,
)

# FLASK APP SETUP
app = Flask(__name__)

# TRAIN MODEL ON STARTUP
# model is trained once when server starts
print("\nInitialising — loading data and training model...")

_df = load_data('data/salary_data.csv')
_df = encode_features(_df)
_X, _y = prepare_features(_df)
_X_train, _X_test, _y_train, _y_test = split_data(_X, _y)
model = train_model(_X_train, _y_train)

# Build sorted list of all job titles for dropdown menu in the HTML form.
ALL_JOB_TITLES = sorted(le_job_title.classes_.tolist())
# ["Bachelor's", "Master's", "PhD"]
EDUCATION_OPTIONS = le_education.classes_.tolist()
# ["Female", "Male"]
GENDER_OPTIONS = le_gender.classes_.tolist()

print("Model ready. Starting web server...\n")


# ROUTES

@app.route('/', methods=['GET'])
def index():
    """
        Render the home page with the prediction form.

        On a GET request (user opening the page in a browser), Flask renders
        index.html and passes the dropdown data so the form can be populated.
        No prediction is shown on the initial page load.
    """
    return render_template(
        'index.html',
        job_titles=ALL_JOB_TITLES,
        education_options=EDUCATION_OPTIONS,
        gender_options=GENDER_OPTIONS,
        prediction=None,
        error=None,
        form_data={}
    )


@app.route('/predict', methods=['POST'])
def predict():
    """
        Handle the prediction form submission.

        When the user fills in the form and clicks 'Predict Salary', the browser
        sends a POST request to this route with the form values. Flask reads them,
        calls predict_salary(), and re-renders the page with the result.

        The form_data dict is passed back so the form fields stay filled in after
        submission - better user experience.
    """
    # Collect all submitted form values
    form_data = {
        'age': request.form.get('age', ''),
        'gender': request.form.get('gender', ''),
        'education_level': request.form.get('education_level', ''),
        'job_title': request.form.get('job_title', ''),
        'years_experience': request.form.get('years_experience', '')
    }

    try:
        # Convert numeric fields from string to float
        age = float(form_data['age'])
        years_experience = float(form_data['years_experience'])
        gender = form_data['gender']
        education_level = form_data['education_level']
        job_title = form_data['job_title']

        # Validate numeric ranges
        if not (18 <= age <= 70):
            raise ValueError("Age must be between 18 and 70.")
        if not (0 <= years_experience <= 40):
            raise ValueError(
                "Years of experience must be between 0 and 40."
            )

        # Run prediction
        predicted = predict_salary(
            model, age, gender, education_level, job_title, years_experience
        )

        # Format the result as a currency string
        result = f"${predicted:,.2f}"

        return render_template(
            'index.html',
            job_titles=ALL_JOB_TITLES,
            education_options=EDUCATION_OPTIONS,
            gender_options=GENDER_OPTIONS,
            prediction=result,
            error=None,
            form_data=form_data
        )

    except ValueError as ve:
        # Catch invalid inputs (e.g. unknown job title, out-of-range values)
        return render_template(
            'index.html',
            job_titles=ALL_JOB_TITLES,
            education_options=EDUCATION_OPTIONS,
            gender_options=GENDER_OPTIONS,
            prediction=None,
            error=str(ve),
            form_data=form_data
        )

    except Exception as e:
        # Catch any unexpected errors
        return render_template(
            'index.html',
            job_titles=ALL_JOB_TITLES,
            education_options=EDUCATION_OPTIONS,
            gender_options=GENDER_OPTIONS,
            prediction=None,
            error=f"Unexpected error: {str(e)}",
            form_data=form_data
        )


# Program Entry Point
if __name__ == '__main__':
    app.run(debug=True)
