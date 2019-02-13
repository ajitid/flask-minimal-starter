from flask_cors import CORS as Cors

from app import app
from config import CORS_API_ORIGINS

cors = Cors(app, resources={
    r"/api/*": {
        "origins": CORS_API_ORIGINS
    }
})
