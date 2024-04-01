import seaborn as sns
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
# load in the carcrash data set
car_crashes = sns.load_dataset('car_crashes')

#  adjust columns in list in the StandardScaler from the dataset features the dataset's features.
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), ['alcohol', 'not_distracted', 'no_previous', 'ins_premium', 'ins_losses']),
    ])

# define the model
model = Pipeline(steps=[('preprocessor', preprocessor),
                        ('regressor', RandomForestRegressor())])

# split the data into separate parts to train and test the ml model
X = car_crashes.drop('total', axis=1) 
y = car_crashes['total']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# train model
model.fit(X_train, y_train)

# predict and evaluate
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")
