import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Load data from a CSV file into a table-like structure called DataFrame
price_data = pd.read_csv('realtor-data.csv')

# Drop rows with missing values in 'price' column
price_data.dropna(subset=['price'], inplace=True)

# Select the columns 'bed', 'bath', 'acre_lot' to use for predicting 'price'.
# Convert their values to numbers and replace any missing or invalid entries with zero.
X = price_data[['bed', 'bath', 'acre_lot']].apply(pd.to_numeric, errors='coerce').fillna(0)
y = price_data['price'].apply(pd.to_numeric, errors='coerce').fillna(0)

# Split the data into two parts: one part for training the model, and one part for testing its predictions.
# Here, 70% of the data is used for training and 30% for testing.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Create a machine learning model based on random forests, which is a method that uses multiple decision trees.
rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)

# Teach the model to predict 'Market Cap' using the training data.
rf_regressor.fit(X_train, y_train)

# Use the trained model to predict 'Market Cap' for the testing data.
y_pred = rf_regressor.predict(X_test)

# Calculate and print the mean squared error for the model's predictions.
# The mean squared error tells us how close the model's predictions are to the actual values, where lower numbers are better.
mse = mean_squared_error(y_test, y_pred)
print('Model MSE:', mse)

# In a real application, you would save the trained model to a file here.
# But since this code is for integration with a Flask web server, we skip that part.


# status,bed,bath,acre_lot,city,state,zip_code,house_size,prev_sold_date,price
# for_sale,3.0,2.0,0.12,Adjuntas,Puerto Rico,601.0,920.0,,105000.0
# for_sale,4.0,2.0,0.08,Adjuntas,Puerto Rico,601.0,1527.0,,80000.0