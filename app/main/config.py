import os

# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@postgres:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SMS4FREE_KEY = 'J2IX1eEa9'
    SMS4FREE_USER = '0525236451'
    SMS4FREE_PASSWORD = '66534228'
