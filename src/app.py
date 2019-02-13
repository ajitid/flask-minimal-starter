from flask import Flask

app = Flask(__name__)

from config import Config
app.config.from_object(Config)

import handlers
import models
import routes
