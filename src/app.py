from flask import Flask

# from flask_jwt_extended import jwt_optional

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

import handlers
import models
import routes


# @app.before_request
# @jwt_optional
# def before_request():
#     pass
