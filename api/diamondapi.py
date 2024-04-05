from flask import Flask, request, jsonify, Blueprint
import pandas as pd
# Import necessary machine learning libraries
from sklearn.tree import DecisionTreeClassifier # Example, might not use directly
from sklearn.linear_model import LogisticRegression # Example, might not use directly
from sklearn.metrics import accuracy_score # Example, might not use directly

# Assuming 'model' is loaded or defined elsewhere for predicting diamond prices
from model.diamondmodel import *
from flask import Flask, request, jsonify, Blueprint
import pandas as pd
from model.diamondmodel import model

app = Flask(__name__)
diamond_api = Blueprint('diamond_api', __name__, url_prefix='/api/diamond')

@diamond_api.route('/predict', methods=['POST'])  # Change this to use the blueprint
def predict():
    try:
        data = request.get_json(force=True)
        features = pd.DataFrame(data, index=[0])
        prediction = model.predict(features)
        return jsonify({'prediction': prediction.tolist()})  # Convert numpy array to list
    except Exception as e:
        return jsonify({'error': str(e)})

# Register the blueprint with the Flask app
app.register_blueprint(diamond_api)

if __name__ == '__main__':
    app.run(debug=True)




