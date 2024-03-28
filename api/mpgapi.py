from flask import Flask, request, jsonify, Blueprint
import pandas as pd
# Import the model pipeline created for the MPG dataset
# Assuming 'mpg_model' is the Pipeline object created for predicting MPG values
from model.mpgmodel import model

app = Flask(__name__)
mpg_api = Blueprint('mpg_api', __name__, url_prefix='/api/mpg')

@mpg_api.route('/predict', methods=['POST'])
def predict():
    try:
        # Parse incoming request data
        data = request.get_json(force=True)
        # Convert the received data into a DataFrame
        # The column order should match the order expected by the model
        features = pd.DataFrame(data, index=[0])
        # Predict the MPG value using the model
        prediction = model.predict(features)
        # Convert prediction to list (for JSON response) and return it
        return jsonify({'prediction': prediction.tolist()})
    except Exception as e:
        # In case of error, return the error message
        return jsonify({'error': str(e)})

# Register the blueprint with the Flask app
app.register_blueprint(mpg_api)

if __name__ == '__main__':
    app.run(debug=True)
