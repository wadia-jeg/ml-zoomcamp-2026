# uv is a fast python package manager
# uv venv – Create a virtual environmen
# uv sync – Sync local environment with the uv.lock file
# uv run <script.py> – Run a script inside the project's managed environment

import pickle

with open("05-deployment/homework/pipeline.bin", 'rb') as pipeline_file:
    (pipeline, model) = pickle.load(pipeline_file)

print(pipeline, model)


test_lead = {
    "lead_source": "paid_ads",
    "industry": "technology",
    "employment_status": "employed",
    "location": "north_america",
    "number_of_courses_viewed": 2,
    "annual_income": 79276.0,
    "interaction_count": 4,
    "lead_score": 0.41
}


X_test_lead = pipeline.transform(test_lead)
y_pred = model.predict_proba(X_test_lead)

print(y_pred[:, 1])
