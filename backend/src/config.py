import os
from datetime import timedelta

class Config:
    #Смените на свои данные от базы PostgreSQL
    SQLALCHEMY_DATABASE_URI = 'postgresql://<login>:<password>@localhost:5433/attackbase'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your_jwt_secret_key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)