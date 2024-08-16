from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ExchangeRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(3), nullable=False)
    rate = db.Column(db.Float, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
