from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Config
from utils.exceptions import ApiException

app = Flask(__name__)
app.config.from_object(Config)

app.register_error_handler(ApiException, lambda err: err.to_response())

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)

import models
import routes
