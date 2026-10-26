# -*- coding: utf-8 -*-
"""
# Deployment
"""

import pickle
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

"""### Model Training

1.  #### Data prepartion
"""
print("1. Data Preparation")

data = 'https://raw.githubusercontent.com/alexeygrigorev/mlbookcamp-code/master/chapter-03-churn-prediction/WA_Fn-UseC_-Telco-Customer-Churn.csv'

"""  - #### Data Loading"""

df = pd.read_csv(data)

"""  - #### Data Formating"""


def format(element):
    return element.str.lower().str.replace(" ", "_")


print("Data Formating")

df.columns = format(df.columns)
df.columns

categorical_columns = list(df.dtypes[df.dtypes == 'object'].index)
# categorical_columns

df[categorical_columns] = df[categorical_columns].apply(format)

numerical = ['tenure', 'monthlycharges', 'totalcharges']

categorical = [
    'gender',
    'seniorcitizen',
    'partner',
    'dependents',
    'phoneservice',
    'multiplelines',
    'internetservice',
    'onlinesecurity',
    'onlinebackup',
    'deviceprotection',
    'techsupport',
    'streamingtv',
    'streamingmovies',
    'contract',
    'paperlessbilling',
    'paymentmethod',
]

df.totalcharges = pd.to_numeric(df.totalcharges, errors="coerce")
df.totalcharges = df.totalcharges.fillna(0)

# df.dtypes

df.churn = (df.churn == "yes").astype(int)

dv = DictVectorizer()

"""  - #### Data Splitting"""
print("Data Splitting")


df_full_train, df_test = train_test_split(df, test_size=0.2, random_state=1)

"""2. #### Model Training"""
print("Model Training")


def train(df, y_train, C=1.0):
    dicts = df[numerical + categorical].to_dict(orient="records")

    dv = DictVectorizer(sparse=False)
    X_train = dv.fit_transform(dicts)

    model = LogisticRegression(C=C, max_iter=1000)
    model.fit(X_train, y_train)

    return dv, model


"""3. #### Model Prediction"""
print("Model Prediction")


def predict(df, dv, model):
    dicts = df[numerical + categorical].to_dict(orient="records")

    X = dv.transform(dicts)

    y_pred = model.predict_proba(X)[:, 1]

    return y_pred


"""4. #### Model Evluation"""

C = 1.0
n_splits = 5

# TODO

kfold = KFold(n_splits=n_splits, shuffle=True, random_state=1)

scores = []

for train_idx, val_idx in kfold.split(df_full_train):
    df_train = df_full_train.iloc[train_idx]
    df_val = df_full_train.iloc[val_idx]

    y_train = df_train.churn.values
    y_val = df_val.churn.values

    dv, model = train(df_train, y_train, C=C)
    y_pred = predict(df_val, dv, model)

    auc = roc_auc_score(y_val, y_pred)
    scores.append(auc)

print('C=%s %.3f +- %.3f' % (C, np.mean(scores), np.std(scores)))

scores

dv, model = train(df_full_train, df_full_train.churn.values, C=1.0)
y_pred = predict(df_test, dv, model)

y_test = df_test.churn.values
auc = roc_auc_score(y_test, y_pred)
auc

"""### Model Saving"""


output_file = "modelC=%s.bin" % C
output_file

# f_out = open(output_file, "wb")
# pickle.dump((dv, model), output_file)
# f_out.close()

# Closes the file automatically
with open(output_file, "wb") as f_out:
    pickle.dump((dv, model), f_out)

"""### Model Loading"""


# model_file = "modelC=1.0.bin"

# with open(model_file, "rb") as f_in:
#     (dv, model) = pickle.load(f_in)

# dv, model

# """### Making Request"""

# customer = {
#     'gender': 'female',
#     'seniorcitizen': 0,
#     'partner': 'yes',
#     'dependents': 'no',
#     'phoneservice': 'no',
#     'multiplelines': 'no_phone_service',
#     'internetservice': 'dsl',
#     'onlinesecurity': 'no',
#     'onlinebackup': 'yes',
#     'deviceprotection': 'no',
#     'techsupport': 'no',
#     'streamingtv': 'no',
#     'streamingmovies': 'no',
#     'contract': 'month-to-month',
#     'paperlessbilling': 'yes',
#     'paymentmethod': 'electronic_check',
#     'tenure': 1,
#     'monthlycharges': 29.85,
#     'totalcharges': 29.85
# }

# X_customer = dv.transform([customer])
# # X_customer

# model.predict_proba(X_customer)[0, 1]
