from app import app

from . import auth

app.register_blueprint(auth.mod, url_prefix="/api/auth")
