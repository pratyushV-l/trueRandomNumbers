import time
import random
import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

def get_system_uptime():
    return time.time() - time.monotonic()

def get_external_random_number():
    response = requests.get('https://www.random.org/integers/?num=1&min=0&max=100&col=1&base=10&format=plain&rnd=new')
    if response.status_code == 200:
        return int(response.text.strip())
    else:
        return 0  # Fallback in case of API failure

def get_solar_radiation(lat, lon, api_key):
    url = f'https://api.openweathermap.org/data/2.5/solar_radiation?lat={lat}&lon={lon}&appid={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['global_horizontal_irradiance']
    else:
        return 0  # Fallback in case of API failure

def get_stock_price(symbol):
    url = f'https://finnhub.io/api/v1/quote?symbol={symbol}&token=your_finnhub_api_key'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['c']  # Current price
    else:
        return 0  # Fallback in case of API failure
        
def get_traffic_data(lat, lon, api_key):
    url = f'https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point={lat},{lon}&key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['flowSegmentData']['currentSpeed']
    else:
        return 0  # Fallback in case of API failure
        
def get_news_headlines(api_key):
    url = f'https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return len(data['articles'])  # Number of articles
    else:
        return 0  # Fallback in case of API failure
    
def get_astronomy_data(api_key):
    url = f'https://api.nasa.gov/planetary/apod?api_key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return len(data['title'])  # Length of the title of the picture of the day
    else:
        return 0  # Fallback in case of API failure

def generate_random_number(api_key, stock_symbol, news_api_key, traffic_api_key, astronomy_api_key):
    uptime = get_system_uptime()
    external_random = get_external_random_number()
    solar_radiation = get_solar_radiation(12.9716, 77.5946, api_key)  # Example coordinates for Bengaluru
    stock_price = get_stock_price(stock_symbol)
    traffic_speed = get_traffic_data(12.9716, 77.5946, traffic_api_key) #Also example for Bengaluru
    news_headlines = get_news_headlines(news_api_key)
    astronomy_val = get_astronomy_data(astronomy_api_key)
    current_time = time.time()
    random_factor = random.random()
    seed = int((uptime + external_random + traffic_speed + news_headlines + astronomy_val + solar_radiation + stock_price + current_time + random_factor) * 1000) % 100
    random_number = (seed * 9301 + 49297) % 233280
    return random_number / 233280

@app.route('/', methods=['GET', 'POST'])
def index():
    api_key = 'your_openweather_api_key'  # Replace with your actual API key
    traffic_api_key = 'your_tomtom_api_key'
    news_api_key = 'your_news_api_api_key
    astronomy_api_key = 'your_nasa_api_key'

    stock_symbol = 'AAPL'  # Default value
    if request.method == 'POST':
        stock_symbol = request.form.get('stock_symbol', 'AAPL').upper()

    random_number = generate_random_number(api_key, stock_symbol, news_api_key, traffic_api_key, astronomy_api_key)
    return render_template_string('''
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <title>Random Number Generator</title>
            <style>
              body {
                font-family: Arial, sans-serif;
                background-color: #f8f9fa;
                color: #343a40;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
              }
              .container {
                text-align: center;
                background: #ffffff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
              }
              h1 {
                margin-bottom: 20px;
              }
              p {
                font-size: 1.5em;
                margin-bottom: 20px;
              }
              input[type="text"] {
                padding: 10px;
                font-size: 1em;
                margin-bottom: 20px;
                border: 1px solid #ccc;
                border-radius: 5px;
                width: 200px;
              }
              button {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 1em;
                border-radius: 5px;
                cursor: pointer;
              }
              button:hover {
                background-color: #0056b3;
              }
            </style>
          </head>
          <body>
            <div class="container">
              <h1>Random Number Generator</h1>
              <form method="post">
                <input type="text" name="stock_symbol" placeholder="Enter stock symbol (e.g., AAPL)" value="{{ stock_symbol }}">
                <br>
                <button type="submit">Generate Number</button>
              </form>
              <p>Random Number: {{ random_number }}</p>
            </div>
          </body>
        </html>
    ''', random_number=random_number, stock_symbol=stock_symbol)

if __name__ == '__main__':
    app.run(debug=True)
