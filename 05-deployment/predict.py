#!/bin/user/env python

import pickle
from flask import Flask, request, jsonify

model_file = "modelC=1.0.bin"

with open(model_file, "rb") as f_in:
    (dv, model) = pickle.load(f_in)

dv, model

app = Flask('ping')


@app.route('/predict', methods=['POST'])
def predict():
    # Get the customer fro the request as json
    customer = request.get_json()

    # Transform the customer using DictVectorizer
    X_customer = dv.transform([customer])

    # Predict the churn probablity using the model
    y_pred = model.predict_proba(X_customer)[0, 1]

    # Decide whetjer to send a churn message or not
    churn = y_pred >= 0.5

    response = {
        "churn_probablity": y_pred,
        "churn": bool(churn)
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9696, debug=True)

# Example of a requets
"""
{
    "gender": "female",
    "seniorcitizen": 0,
    "partner": "yes",
    "dependents": "no",
    "phoneservice": "no",
    "multiplelines": "no_phone_service",
    "internetservice": "dsl",
    "onlinesecurity": "no",
    "onlinebackup": "yes",
    "deviceprotection": "no",
    "techsupport": "no",
    "streamingtv": "no",
    "streamingmovies": "no",
    "contract": "month-to-month",
    "paperlessbilling": "yes",
    "paymentmethod": "electronic_check",
    "tenure": 1,
    "monthlycharges": 29.85,
    "totalcharges": 29.85
}
"""
# In production WSGI server should used with gunicorn
# pip install gunicorn
# gunicorn --bind 0.0.0.0:9696 predict:app

# !! For windows use waitress instead of gunicorn
# waitress-server --listen=0.0.0.0:9696 predict:app
