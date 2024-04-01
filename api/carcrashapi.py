from flask import Flask, request, jsonify, Blueprint
import pandas as pd
# import the RandomForestRegressor model pipeline we've created
from model.carcrashmodel import *

app = Flask(__name__)
car_crash_api = Blueprint('car_crash_api', __name__, url_prefix='/api/car_crash')

@car_crash_api.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        # make sure data is in the correct format for prediction (
        features = pd.DataFrame(data, index=[0])
        prediction = model.predict(features)
        # Convert for json
        return jsonify({'prediction': prediction.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)})

# Register the blueprint with the Flask app
# app.register_blueprint(car_crash_api)

if __name__ == '__main__':
    app.run(debug=True)