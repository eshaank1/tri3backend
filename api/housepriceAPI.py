from flask import Flask, request, jsonify, Blueprint
import pandas as pd
from model.housepriceMLmodel import *

# Initialize a new web application using Flask.
app = Flask(__name__)

# Create a blueprint for our API. Think of this as a component of the app that handles all 'stock' related operations.
houseprice_api = Blueprint('houseprice_api', __name__, url_prefix='/api/houseprice')

@houseprice_api.route('/predict', methods=['POST'])
def predict_house_price():
    try:
        # Extract the data sent by the user.
        data = request.json
        
        # Get the input features from the data.
        bedrooms = float(data.get('bedrooms', 0))
        bathrooms = float(data.get('bathrooms', 0))
        acre_lot = float(data.get('acre_lot', 0))
        
        # Prepare the features for prediction.
        features = [[bedrooms, bathrooms, acre_lot]]
        
        # Use the model to predict the house price based on the provided features.
        predicted_price = rf_regressor.predict(features)[0]
        
        # Format the predicted price to two decimal places.
        formatted_price = f"{predicted_price:.2f}"
        
        # Create a response object containing the prediction.
        response = {'predicted_price': formatted_price}
        return jsonify(response), 200
    except Exception as e:
        # If something goes wrong, send back an error message with status code 400 (Bad Request).
        return jsonify({'error': str(e)}), 400

# Register the blueprint with the main app.
app.register_blueprint(houseprice_api)

if __name__ == '__main__':
    app.run(debug=True)

