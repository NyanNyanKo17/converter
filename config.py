import os

class Config:
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(os.getcwd(), "currency.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
