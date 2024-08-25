import time
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

def generate_random_number():
    uptime = get_system_uptime()
    external_random = get_external_random_number()
    current_time = time.time()
    seed = int((uptime + external_random + current_time) * 1000) % 100
    random_number = (seed * 9301 + 49297) % 233280
    return random_number / 233280

@app.route('/')
def index():
    random_number = generate_random_number()
    return render_template_string('''
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <title>Random Number Generator</title>
          </head>
          <body>
            <div style="text-align: center; margin-top: 50px;">
              <h1>Random Number Generator</h1>
              <p>Random Number: {{ random_number }}</p>
              <button onclick="window.location.reload();">Generate New Number</button>
            </div>
          </body>
        </html>
    ''', random_number=random_number)

if __name__ == '__main__':
    app.run(debug=True)
