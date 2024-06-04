import seaborn as sns
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Load the dataset
diamonds = sns.load_dataset('diamonds')

# Basic preprocessing
# Convert categorical variables into dummy variables
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), ['carat', 'depth', 'table', 'x', 'y', 'z']),
        ('cat', OneHotEncoder(), ['cut', 'color', 'clarity'])
    ])

# Define the model
model = Pipeline(steps=[('preprocessor', preprocessor),
                        ('regressor', RandomForestRegressor())])

# Split the data
X = diamonds.drop('price', axis=1)
y = diamonds['price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")