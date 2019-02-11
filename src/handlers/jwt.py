from flask_jwt_extended import JWTManager

from app import app
from models.user import User

jwt = JWTManager(app)

# FIXME expire time of JWT and cookie-session, refresh token needed in JWT?

# LATER for better way and perf, https://flask-jwt-extended.readthedocs.io/en/latest/blacklist_and_token_revoking.html
jwt_blacklist = set()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token["jti"]
    return jti in jwt_blacklist


@jwt.user_loader_callback_loader
def user_loader_callback(id):
    return User.query.get(id)
