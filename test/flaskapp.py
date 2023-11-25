from flask import Flask, render_template, request, redirect, flash
import requests
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use Agg backend for Matplotlib
import matplotlib.pyplot as plt
from datetime import datetime
import os
from io import BytesIO
import base64

app = Flask(__name__, template_folder='templates')
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'your-secret-key'

static_folder = os.path.join(app.root_path, 'static')
os.makedirs(static_folder, exist_ok=True)

def generate_plot(stock_symbol, chart_type, time_series_data):
    dates = list(time_series_data.keys())
    prices = [float(time_series_data[date]["4. close"]) for date in dates]

    plt.figure(figsize=(10, 6))
    if chart_type == "1":
        plt.bar(dates, prices, label="Stock Price", color="g")
    else:
        plt.plot(dates, prices, label="Stock Price", color="b")

    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title(f"Stock Price Chart ({'Bar' if chart_type == '1' else 'Line'})")
    plt.xticks(rotation=45)
    plt.legend()

    # Save the plot to a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()

    # Convert the image stream to base64 encoding
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')

    # Move the cursor to the beginning of the stream
    image_stream.seek(0)

    return image_base64

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chart', methods=['POST'])
def generate_chart():
    try:
        stock_symbol = request.form['stock_symbol']
        chart_type = request.form['chart_type']

        base_url = "https://www.alphavantage.co/query?"
        api_key = "CRF5E6TEAFQOQWZY"

        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": stock_symbol,
            "apikey": api_key,
        }

        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()
            time_series_data = data.get("Time Series (Daily)")

            if time_series_data is None:
                return "No data available for the selected stock symbol."

            # Generate plot
            image_stream = generate_plot(stock_symbol, chart_type, time_series_data)

            return render_template('result.html', image_stream=image_stream, stock_symbol=stock_symbol)
        else:
            flash("Failed to retrieve data from Alpha Vantage API.", 'error')
            return redirect('/')
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'error')
        return redirect('/')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5003)