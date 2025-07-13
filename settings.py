import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
    SECRET_KEY = os.getenv('SECRET_KEY', '17268wt1782187t2871et8t387te')
    DISK_TOKEN = os.getenv('DISK_TOKEN', 'your token')
    API_HOST = os.getenv('API_HOST', 'https://cloud-api.yandex.net/')
    API_VERSION = os.getenv('API_VERSION', 'v1')
