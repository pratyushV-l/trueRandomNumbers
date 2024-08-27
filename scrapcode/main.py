import time
import random
import requests
from flask import Flask, render_template_string, request
import math

app = Flask(__name__)

# Helper functions

# Calculates how long the system (or the code) has been running for
def get_system_uptime():
    return time.time() - time.monotonic()

# Uses an API to get a random number; this is an extra feature in case other APIs fail
def get_external_random_number():
    response = requests.get('https://www.random.org/integers/?num=1&min=0&max=100&col=1&base=10&format=plain&rnd=new')
    if response.status_code == 200:
        return int(response.text.strip())
    else:
        return 0  # Fallback in case of API failure

# Calculates the amount of solar radiation at the given latitude and longitude
def get_solar_radiation(lat, lon, api_key):
    url = f'https://api.openweathermap.org/data/2.5/solar_radiation?lat={lat}&lon={lon}&appid={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['global_horizontal_irradiance']
    else:
        return 0  # Fallback in case of API failure

# Retrieves the current stock price for the given stock symbol
def get_stock_price(symbol):
    url = f'https://finnhub.io/api/v1/quote?symbol={symbol}&token=api'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['c']  # Current price
    else:
        return 0  # Fallback in case of API failure

# Retrieves traffic data (current speed) for the given latitude and longitude
def get_traffic_data(lat, lon, api_key):
    url = f'https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point={lat},{lon}&key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['flowSegmentData']['currentSpeed']
    else:
        return 0  # Fallback in case of API failure

# Retrieves the number of current news headlines for a specified country
def get_news_headlines(api_key):
    url = f'https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return len(data['articles'])  # Number of articles
    else:
        return 0  # Fallback in case of API failure

# Retrieves the length of NASA's Astronomy Picture of the Day title
def get_astronomy_data(api_key):
    url = f'https://api.nasa.gov/planetary/apod?api_key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return len(data['title'])  # Length of the title of the picture of the day
    else:
        return 0  # Fallback in case of API failure

# Combines all the above data to generate a random number within a specified range
def generate_random_number(api_key, stock_symbol, news_api_key, traffic_api_key, astronomy_api_key, lat, lon, start_num, end_num):
    uptime = get_system_uptime()
    external_random = get_external_random_number()
    solar_radiation = get_solar_radiation(lat, lon, api_key)
    stock_price = get_stock_price(stock_symbol)
    traffic_speed = get_traffic_data(lat, lon, traffic_api_key)
    news_headlines = get_news_headlines(news_api_key)
    astronomy_val = get_astronomy_data(astronomy_api_key)
    current_time = time.time()
    random_factor = random.random()
    
    # Calculate a seed value based on various data points and random factors
    seed = int((uptime + external_random + traffic_speed + news_headlines + astronomy_val + solar_radiation + stock_price + current_time + random_factor) * 1000) % 100
    
    # Generate a pseudo-random number using the seed
    random_number = ((seed * 9301 + 49297) % 233280)
    final_number = math.floor((random_number / 233280) * (end_num + 1 - start_num) + start_num)
    
    return final_number

# Rolls a die (1 to 6) using a random number generator
def dice_rolled():
    die_val = generate_random_number('apis')
    return die_val

@app.route('/', methods=['GET', 'POST'])
def index():
    # API keys

    # Default values
    stock_symbol = 'AAPL'
    lat = '12.9716'
    lon = '77.5946'
    start_num = 0
    end_num = 100
    random_number = None
    dice_result = None
    randNum2 = None

    if request.method == 'POST':
        if 'generate_number' in request.form:
            # Retrieve and process form data
            stock_symbol = request.form.get('stock_symbol', 'AAPL').upper()
            lat = request.form.get('latitude', '12.9716')
            lon = request.form.get('longitude', '77.5946')
            start_num = int(request.form.get('start_num', '0'))
            end_num = int(request.form.get('end_num', '100'))

            # Generate random number
            random_number = generate_random_number(api_key, stock_symbol, news_api_key, traffic_api_key, astronomy_api_key, lat, lon, start_num, end_num)
        elif 'roll_dice' in request.form:
            # Roll dice
            dice_result = dice_rolled()
        else:
            button_value = request.form.get('buttonvalue')
            if button_value:
                start_num = 1
                end_num = int(button_value)
                randNum2 = generate_random_number(api_key, stock_symbol, news_api_key, traffic_api_key, astronomy_api_key, lat, lon, start_num, end_num)

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
                background-color: #fff3b0;
                color: #343a40;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
              }
              .container {
                text-align: center;
                background: #e09f3e;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
              }
              h1 {
                margin-bottom: 20px;
                color: 540b0e
              }
              p {
                font-size: 1.5em;
                margin-bottom: 20px;
                color: 540b0e
              }
              input[type="text"] {
                padding: 10px;
                font-size: 1em;
                color: white;
                margin-bottom: 20px;
                background: #335c67;
                border: 1px solid #ccc;
                border-radius: 5px;
                width: 200px;
              }
              button {
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 1em;
                border-radius: 5px;
                cursor: pointer;
                margin: 5px;
                transition: background-color 0.3s ease;
              }
              .generate-button {
                background-color: #335c67;
              }
              .generate-button:hover {
                background-color: #0056b3;
              }
              .roll-button {
                background-color: #9e2a2b;
                font-size: 0.9em; /* Smaller font size for the Roll Dice button */
                padding: 8px 16px; /* Smaller padding for the Roll Dice button */
              }
              .roll-button:hover {
                background-color: #218838;
              }
              .small-button {
                background-color: #9e2a2b;
                font-size: 0.7em;
                padding: 5px 10px;
                margin-bottom: 10px;
              }
              .small-button:hover {
                background-color: #218838;
              }
              .note {
                margin-top: 20px;
                font-size: 1em;
                color: #6c757d;
              }
              #dice-result {
                font-size: 1.5em;
                margin-top: 20px;
              }
            </style>
          </head>
          <body>
            <div class="container">
              <h1>Random Number Generator</h1>
              <form method="post">
                <input type="text" name="stock_symbol" placeholder="Enter stock symbol (e.g., AAPL)" value="{{ stock_symbol }}">
                <br>
                <input type="text" name="latitude" placeholder="Enter latitude" value="{{ lat }}">
                <br>
                <input type="text" name="longitude" placeholder="Enter longitude" value="{{ lon }}">
                <br>
                <input type="text" name="start_num" placeholder="Start Number" value="{{ start_num }}">
                <br>
                <input type="text" name="end_num" placeholder="End Number" value="{{ end_num }}">
                <br>
                <button type="submit" name="buttonvalue" value=2 class="small-button">2</button>
                <button type="submit" name="buttonvalue" value=3 class="small-button">3</button>
                <button type="submit" name="buttonvalue" value=4 class="small-button">4</button>
                <button type="submit" name="buttonvalue" value=5 class="small-button">5</button>
                <button type="submit" name="buttonvalue" value=10 class="small-button">10</button>
                <button type="submit" name="buttonvalue" value=15 class="small-button">15</button>
                <button type="submit" name="buttonvalue" value=50 class="small-button">50</button>
                <button type="submit" name="buttonvalue" value=100 class="small-button">100</button>
                <button type="submit" name="buttonvalue" value=500 class="small-button">500</button>
                <button type="submit" name="buttonvalue" value=1000 class="small-button">1000</button>
                <button type="submit" name="buttonvalue" value=999999 class="small-button">999999</button>
                <br>
                <button type="submit" name="generate_number" class="generate-button">Generate Random Number</button>
                <br>
                <button type="submit" name="roll_dice" class="roll-button">Roll Dice</button>
              </form>
              {% if random_number is not none %}
                <p>Random Number: {{ random_number }}</p>
              {% endif %}
              {% if dice_result is not none %}
                <div id="dice-result">Dice Rolled: {{ dice_result }}</div>
              {% endif %}
              {% if randNum2 is not none %}
                <p>Random Number: {{ randNum2 }}</p>
              {% endif %}
              <div class="note">Note: Use stock symbols (e.g., AAPL) and valid coordinates for accurate results.</div>
            </div>
          </body>
        </html>
    ''', random_number=random_number, dice_result=dice_result, stock_symbol=stock_symbol, lat=lat, lon=lon, start_num=start_num, end_num=end_num, randNum2=randNum2)

if __name__ == '__main__':
    app.run(debug=True)
