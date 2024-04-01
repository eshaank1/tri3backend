import seaborn as sns
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

# Load the dataset
mpg = sns.load_dataset('mpg')

# Check for missing values and decide on a strategy
# For simplicity, we'll impute missing values for numerical columns
# and drop rows with missing categorical values for this example

# Basic preprocessing
# Convert categorical variables into dummy variables and impute missing values for numerical features
preprocessor = ColumnTransformer(
    transformers=[
        ('num', Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler())]), ['cylinders', 'displacement', 'horsepower', 'weight', 'acceleration']),
        ('cat', OneHotEncoder(), ['origin', 'model_year'])
    ])

# Define the model
model = Pipeline(steps=[('preprocessor', preprocessor),
                        ('regressor', RandomForestRegressor())])

# We drop rows with missing target ('mpg') values and any rows with missing categorical values that we can't easily impute
mpg.dropna(subset=['mpg', 'origin', 'model_year'], inplace=True)

X = mpg.drop('mpg', axis=1).select_dtypes(include=['float64', 'int64', 'object'])
y = mpg['mpg']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")
