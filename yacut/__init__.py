from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from settings import Config


app = Flask(__name__, static_folder='static')
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.json.ensure_ascii = False


from . import views