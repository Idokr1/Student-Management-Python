import os

# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']
key = "MyJwtLovelyKey1234567890!!1234567890"
class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@postgres:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SMS4FREE_KEY = 'J2IX1eEa9'
    SMS4FREE_USER = '0525236451'
    SMS4FREE_PASSWORD = '66534228'
    AWS_ACCESSKEY = 'AKIA6PS436XZW5V5FE5P'
    AWS_SECRETKEY= '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'
    BUCKET_URL = 'files.handson.academy'

