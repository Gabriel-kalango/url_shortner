import os
from decouple import config
from datetime import timedelta

class Config:
    SECRET_KEY = config('SECRET_KEY', 'secret')
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')
    UPLOADED_IMAGES_DEST=os.path.join("api","static","images")
    MAX_CONTENT_LENGTH=10*1024*1024
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300
    PROPAGATE_EXCEPTIONS=True

class DevConfig(Config):
    DEBUG = config('DEBUG', cast=bool)
    SQLALCHEMY_ECHO=True
    SQLALCHEMY_DATABASE_URI= "sqlite:///food.db"
    

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI=config('DATABASE_URL')
    DEBUG=False
    SQLALCHEMY_TRACK_MODIFICATIONS=False

config_dict = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'test': TestConfig
}