from flask import Flask, request, jsonify, Blueprint
import pandas as pd
import sqlite3
from model.housepriceMLmodel import *

# Initialize a new web application using Flask.
app = Flask(__name__)

DATABASE = 'savedsettings.db'

# Create a table to store settings if it doesn't exist.
def create_settings_table():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS settings (
                            id INTEGER PRIMARY KEY,
                            bedrooms REAL,
                            bathrooms REAL,
                            acre_lot REAL
                          )''')
        conn.commit()

# Call the function to create the settings table.
create_settings_table()

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
    
@houseprice_api.route('/settings', methods=['POST'])
def save_settings():
    try:
        # Extract the data sent by the user.
        data = request.json
        
        # Get the input features from the data.
        bedrooms = float(data.get('bedrooms', 0))
        bathrooms = float(data.get('bathrooms', 0))
        acre_lot = float(data.get('acre_lot', 0))
        
        # Connect to the database.
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            
            # Insert or replace the settings in the database.
            cursor.execute('''INSERT OR REPLACE INTO settings (id, bedrooms, bathrooms, acre_lot) 
                              VALUES (1, ?, ?, ?)''', (bedrooms, bathrooms, acre_lot))
            
            # Commit the transaction.
            conn.commit()
        
        # Return a success message.
        return jsonify({'message': 'Settings saved successfully'}), 200
    except Exception as e:
        # If something goes wrong, send back an error message with status code 400 (Bad Request).
        return jsonify({'error': str(e)}), 400

@houseprice_api.route('/settings', methods=['GET'])
def get_settings():
    try:
        # Connect to the database.
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            
            # Fetch the settings from the database.
            cursor.execute('''SELECT * FROM settings WHERE id = 1''')
            row = cursor.fetchone()
            
            if row:
                # If settings exist, create a response object containing the settings.
                response = {
                    'bedrooms': row[1],
                    'bathrooms': row[2],
                    'acre_lot': row[3]
                }
                return jsonify(response), 200
            else:
                # If no settings found, return an empty response.
                return jsonify({}), 200
    except Exception as e:
        # If something goes wrong, send back an error message with status code 400 (Bad Request).
        return jsonify({'error': str(e)}), 400



# Register the blueprint with the main app.
app.register_blueprint(houseprice_api)

if __name__ == '__main__':
    app.run(debug=True)

