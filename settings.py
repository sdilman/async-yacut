import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']
    SECRET_KEY = os.environ['SECRET_KEY']
    DISK_TOKEN = os.environ['DISK_TOKEN']