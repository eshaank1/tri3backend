from flask import Flask, request, jsonify, Blueprint
import pandas as pd
from model.mpgmodel import model

app = Flask(__name__)
mpg_api = Blueprint('mpg_api', __name__, url_prefix='/api/mpg')

@mpg_api.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        
        # Convert numeric 'origin' values to strings based on a predefined mapping
        origin_map = {'1': 'usa', '2': 'europe', '3': 'japan'}
        if 'origin' in data:
            data['origin'] = origin_map.get(str(data['origin']), data['origin'])
        
        features = pd.DataFrame(data, index=[0])
        
        # Ensure that 'model_year' is treated in the manner consistent with model training
        # This step would need adjustments based on the actual training treatment of 'model_year'
        
        print("DataFrame structure from API input:", features)
        
        prediction = model.predict(features)
        
        prediction_list = prediction.tolist()
        print("Prediction result:", prediction_list)
        
        return jsonify({'prediction': prediction_list})
    except Exception as e:
        print("Error during prediction:", str(e))
        return jsonify({'error': str(e)})

app.register_blueprint(mpg_api)

if __name__ == '__main__':
    app.run(debug=True)