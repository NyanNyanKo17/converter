from flask import Flask, render_template, jsonify, request
from models import db, ExchangeRate
from config import Config
import requests
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

def update_exchange_rates():
    response = requests.get(API_URL)
    data = response.json()
    rates = data.get('rates', {})
    for currency, rate in rates.items():
        existing_rate = ExchangeRate.query.filter_by(currency=currency).first()
        if existing_rate:
            existing_rate.rate = rate
            existing_rate.updated_at = datetime.utcnow()
        else:
            new_rate = ExchangeRate(currency=currency, rate=rate)
            db.session.add(new_rate)
    db.session.commit()

@app.route('/update-rates', methods=['GET'])
def update_rates():
    update_exchange_rates()
    return jsonify({'message': 'Exchange rates updated successfully!'})

@app.route('/last-update', methods=['GET'])
def last_update():
    last_rate = ExchangeRate.query.order_by(ExchangeRate.updated_at.desc()).first()
    if last_rate:
        return jsonify({'last_updated': last_rate.updated_at})
    return jsonify({'message': 'No rates found'})

@app.route('/convert', methods=['POST'])
def convert_currency():
    data = request.json
    from_currency = data['from']
    to_currency = data['to']
    amount = data['amount']

    from_rate = ExchangeRate.query.filter_by(currency=from_currency).first().rate
    to_rate = ExchangeRate.query.filter_by(currency=to_currency).first().rate

    converted_amount = (amount / from_rate) * to_rate
    return jsonify({'converted_amount': converted_amount})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
