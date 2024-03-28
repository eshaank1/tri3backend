from flask import Flask, request, jsonify, Blueprint
import pandas as pd
# Import the model pipeline created for the MPG dataset
# Assuming 'model' is the Pipeline object created for predicting MPG values
from model.mpgmodel import model

app = Flask(__name__)
mpg_api = Blueprint('mpg_api', __name__, url_prefix='/api/mpg')

@mpg_api.route('/predict', methods=['POST'])
def predict():
    """
    Predict the MPG (miles per gallon) for a given set of car features.
    
    This endpoint accepts JSON data representing the features of a car and uses
    a pre-trained model to predict the car's MPG. The model expects data in a
    specific format and order, so incoming data is processed accordingly before
    making a prediction.
    
    Returns:
        Flask response object: JSON object containing the predicted MPG values or an error message.
    """
    try:
        # Parse incoming request data to ensure it is received as JSON
        data = request.get_json(force=True)
        # Convert the JSON payload into a pandas DataFrame
        # The column order should match the order expected by the model
        features = pd.DataFrame(data, index=[0])
        # Use the imported 'model' to predict the MPG value based on input features
        prediction = model.predict(features)
        # Convert the prediction to a list for JSON serialization and return the response
        return jsonify({'prediction': prediction.tolist()})
    except Exception as e:
        # Handle any exceptions that occur and return an error message
        return jsonify({'error': str(e)})

# Register the 'mpg_api' blueprint with the Flask application
# This integrates our defined routes into the Flask app
app.register_blueprint(mpg_api)

if __name__ == '__main__':
    """
    Main entry point of the Flask application.
    
    When this script is executed as the main program, it starts a Flask web server
    in debug mode. Debug mode enables live reloading and provides a debugger interface,
    making development and troubleshooting more efficient.
    """
    app.run(debug=True)
