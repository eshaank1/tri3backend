import http.client
import json
from urllib.parse import quote

# Initialize the stock data fetch process
def initStockData():
    print("Stock data initialization done!!!")

# Your Alpha Vantage API key
access_key = "NN5Z6YJMAC2LMUNP"

def getStockData(symbol):
    conn = http.client.HTTPSConnection("www.alphavantage.co")
    payload = ''
    headers = {}
    encodedSymbol = quote(symbol)
    # Using the TIME_SERIES_DAILY function as an example. Modify as needed.
    conn.request("GET", f"/query?function=TIME_SERIES_DAILY&symbol={encodedSymbol}&apikey={access_key}", payload, headers)
    res = conn.getresponse()
    data = res.read()
    decodedString = data.decode("utf-8")
    j = json.loads(decodedString)
    # Extracting and returning only the most recent day's data for simplicity.
    # Adjust according to your needs.
    try:
        latestDate = next(iter(j['Time Series (Daily)']))
        latestData = j['Time Series (Daily)'][latestDate]
        return {
            "symbol": symbol,
            "date": latestDate,
            "open": latestData['1. open'],
            "high": latestData['2. high'],
            "low": latestData['3. low'],
            "close": latestData['4. close'],
            "volume": latestData['5. volume']
        }
    except KeyError:
        # In case the API response does not contain the expected data
        return {"error": "Failed to fetch or parse stock data from Alpha Vantage"}

if __name__ == "__main__":
    # Example usage
    symbol = "AAPL"  # Apple Inc. stock symbol
    stockData = getStockData(symbol)
    print(stockData)
