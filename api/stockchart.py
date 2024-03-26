from flask import Blueprint, jsonify
from flask_restful import Api, Resource
import requests

# Define the Blueprint
stockchart_api = Blueprint('stockchart_api', __name__, url_prefix='/api/stockchart')
api = Api(stockchart_api)

class StockDataAPI(Resource):
    ALPHA_VANTAGE_API_KEY = "NN5Z6YJMAC2LMUNP"  # Replace with your actual API Key
    ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"

    def get(self, symbol):
        # Construct the API request URL for fetching time series data
        params = {
            "function": "TIME_SERIES_DAILY",  # For daily time series data
            "symbol": symbol,
            "apikey": self.ALPHA_VANTAGE_API_KEY
        }
        response = requests.get(self.ALPHA_VANTAGE_BASE_URL, params=params)
        if response.status_code == 200:
            # Successfully fetched the data from Alpha Vantage
            data = response.json()
            # Optional: Transform or filter `data` here as needed
            return jsonify(data)
        else:
            # Handle errors (e.g., bad request, API limit exceeded)
            return {"error": "Failed to fetch data from Alpha Vantage"}, response.status_code

# Add the resource to the API, including a path for the 'symbol' parameter
api.add_resource(StockDataAPI, '/chart/<string:symbol>')
