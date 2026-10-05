import numpy as np
import pandas as pd

data = pd.read_csv("data/car_fuel_efficiency_2026.csv")

#Q1:
pandas_version = pd.__version__
print("Q1/ Pandas Version: ", pandas_version)

#Q2:
data_records = data.shape[0]
print("Q2/ Records Number: ", data_records)

#Q3: 
fuel_types = data["fuel_type"].nunique()
print("Q3/ Fuel Types: ", fuel_types)

#Q4: 
missing_values_total = data.isna().sum()
print("Q4/ Missing Values Total: ", missing_values_total)

#Q5:
max_fuel_efficiency = data["fuel_efficiency_mpg"].max()
print("Q5/ Max Fuel Efficiency ", max_fuel_efficiency)

#Q6:
horsepower_median = data["horsepower"].median()
print("Q6/ Horsepower Median ", horsepower_median)

most_frequent_value =  data["horsepower"].value_counts().index[0]

print("Q6/ Most Frequent Value in the Horsepower column", most_frequent_value)

filled_horsepower_col = data["horsepower"].fillna(most_frequent_value)

new_median = filled_horsepower_col.median()
print("Q6/ New Median ", new_median)

#Q7: 
# Select all the cars from Asia
asia_cars = data[data["origin"] == "Asia"]

# Select only columns vehicle_weight and model_year and the first 7 values
selected_cols = asia_cars[["vehicle_weight", "model_year"]][:7]

# Get the underlying NumPy array. Let's call it X.
X = selected_cols.to_numpy()

# Compute matrix-matrix multiplication between the transpose of X and X
XTX = X.T.dot(X)

# Invert XTX
inverted_XTX = np.linalg.inv(XTX)

# Create an array y
y = np.array([1100, 1300, 800, 900, 1000, 1100, 1200])
# Multiply the inverse of XTX with the transpose of X, and then multiply the result by y
w = inverted_XTX.dot(X.T.dot(y))

# Sum of Weights
print(w.sum())