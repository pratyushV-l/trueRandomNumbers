import time
import random
import requests
from flask import Flask, render_template_string

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

def generate_random_number(api_key):
    uptime = get_system_uptime()
    external_random = get_external_random_number()
    solar_radiation = get_solar_radiation(12.9716, 77.5946, api_key)  # Example coordinates for Bengaluru
    current_time = time.time()
    random_factor = random.random()
    seed = int((uptime + external_random + solar_radiation + current_time + random_factor) * 1000) % 100
    random_number = (seed * 9301 + 49297) % 233280
    return random_number / 233280

@app.route('/')
def index():
    api_key = 'your_openweathermap_api_key'  # Replace with your actual API key
    random_number = generate_random_number(api_key) # Excuse me for the horrendous code hereafter, it is the easiest way to delpoy for me
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
              <p>Random Number: {{ random_number }}</p>
              <button onclick="window.location.reload();">Generate New Number</button>
            </div>
          </body>
        </html>
    ''', random_number=random_number)

# Removed the app.run() line - for the pythonanwhere part
