from flask import Flask, request, jsonify, Blueprint
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import seaborn as sns
from model.titanic import dt, logreg, enc, cols 

app = Flask(__name__)

# Create a Blueprint for the Titanic API
titanic_api = Blueprint('titanic_api', __name__, url_prefix='/api/titanic')

# Load and prepare the Titanic dataset
# titanic_data = sns.load_dataset('titanic')
# titanic_data.drop(['alive', 'who', 'adult_male', 'deck', 'class', 'embark_town'], axis=1, inplace=True)
# titanic_data.dropna(inplace=True)
# titanic_data['sex'] = titanic_data['sex'].apply(lambda x: 1 if x == 'male' else 0)
# titanic_data['alone'] = titanic_data['alone'].apply(lambda x: 1 if x == True else 0)

# # Assume you have already trained your model and it is loaded here
# # For the sake of this example, we retrain the model every time the API is started, which is not efficient.
# # Normally, you would load a pre-trained model here.

# # Preparing the dataset (omitting the one-hot encoding for brevity, you should include it as per your model's training)
# X = titanic_data.drop('survived', axis=1)
# y = titanic_data['survived']
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# # Train the models
# dt = DecisionTreeClassifier()
# dt.fit(X_train, y_train)

# logreg = LogisticRegression()
# logreg.fit(X_train, y_train)

@titanic_api.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract features from the request
        data = request.get_json(force=True)
        features = pd.DataFrame(data, index=[0])

        # Apply one-hot encoding to 'embarked' as was done in the training
        onehot = enc.transform(features[['embarked']]).toarray()
        features = features.join(pd.DataFrame(onehot, columns=cols))
        features.drop(['embarked'], axis=1, inplace=True)

        # Predict with both models
        prediction_dt_proba = dt.predict_proba(features)
        prediction_logreg_proba = logreg.predict_proba(features)

        # Get the survival probability (the second column of the output)
        survival_probability_dt = prediction_dt_proba[0][1]
        survival_probability_logreg = prediction_logreg_proba[0][1]

        # Return both predictions as percentages
        return jsonify({
            'DecisionTreeClassifier Survival Probability': f"{survival_probability_dt:.2%}",
            'LogisticRegression Survival Probability': f"{survival_probability_logreg:.2%}"
        })
    except Exception as e:
        return jsonify({'error': str(e)})


# Register the blueprint with the main app
# app.register_blueprint(titanic_api)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)