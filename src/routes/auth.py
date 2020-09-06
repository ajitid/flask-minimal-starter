from datetime import datetime
from flask import jsonify, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from voluptuous import Schema, Required, REMOVE_EXTRA, In, All, Length, Email
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_raw_jwt, \
    jwt_refresh_token_required
from sqlalchemy import or_

from models.user import User
from handlers.db import db
from handlers.jwt import jwt_blacklist
from helpers.decorators import dataschema
from helpers import status_codes
from helpers.exceptions import ApiException
from helpers.fns import is_email


"""
on why /logout and /token-refresh have POST method and not GET
https://stackoverflow.com/a/14587231/7683365
"""

"""
currently for JWT
/logout doesn't blacklist refresh token
/token-refresh doesn't blacklist access token

from docs: Refresh tokens cannot access an endpoint that is protected with jwt_required() and
access tokens cannot access an endpoint that is protected with jwt_refresh_token_required().

if you need to fix this, one option can be to obtain respective missing token from JSON and then blacklist it

on same note, logout from all devices for cookie-sessions can be achieved using
https://flask-login.readthedocs.io/en/latest/#alternative-tokens
for example, instead of only using user_id as session-id, using a combination of user_id and one-way hash of password
"""

"""
in signup method, username is not checked to only include specific characters
change this according to your needs in dataschema decorator of signup method
"""


mod = Blueprint("auth", __name__)


@mod.route("/")
def index():
    return jsonify({"status": "All set!"})


@mod.route("/check-auth")
def check_auth():
    if not current_user.is_authenticated:
        return jsonify({"authenticated": False})
    user = current_user
    return jsonify({"authenticated": True, "username": user.username})


def get_user_from_username_or_email(username=None, email=None):
    user = User.query.filter(or_(User.username == username, User.email == email)).first()
    return user


def get_jwt_tokens(identity):
    # as JWT don't have sliding mechanism built-in, so long expiry of access and refresh token is used instead
    access_token = create_access_token(identity=identity, expires_delta=datetime.timedelta(days=270))
    refresh_token = create_refresh_token(identity=identity, expires_delta=datetime.timedelta(days=365))
    return {"access_token": access_token, "refresh_token": refresh_token}


@mod.route("/login", methods=["POST"])
@dataschema(
    Schema(
        {
            Required("username_or_email"): str,
            Required("password"): str,
            Required("auth_type"): In(["token", "cookie"]),
        },
        extra=REMOVE_EXTRA,
    )
)
def login(username_or_email, password, auth_type):
    user = None
    if is_email(username_or_email):
        user = get_user_from_username_or_email(email=username_or_email)
    else:
        user = get_user_from_username_or_email(username=username_or_email)
    if user is None or not User.match_password(user, password):
        raise ApiException("Invalid username or password", status_codes.HTTP_401_UNAUTHORIZED)
    if auth_type is "cookie":
        login_user(user, remember=True)
        return "", status_codes.HTTP_204_NO_CONTENT
    elif auth_type is "token":
        tokens = get_jwt_tokens(user.id)
        return jsonify(tokens)
    raise ApiException("Authentication failed", status_codes.HTTP_401_UNAUTHORIZED)


@mod.route('/token-refresh', methods=["POST"])
@jwt_refresh_token_required
def refresh_token():
    user_id = get_jwt_identity()
    if user_id is None:
        raise ApiException("Token generation failed", status_codes.HTTP_401_UNAUTHORIZED)
    jti = get_raw_jwt()["jti"]
    jwt_blacklist.add(jti)
    tokens = get_jwt_tokens(user_id)
    return jsonify(tokens)


@mod.route("/logout", methods=["POST"])
@login_required
def logout():
    if get_jwt_identity() is not None:
        jti = get_raw_jwt()["jti"]
        jwt_blacklist.add(jti)
    else:
        logout_user()
    return "", status_codes.HTTP_204_NO_CONTENT


@mod.route("/signup", methods=["POST"])
@dataschema(
    Schema(
        {
            Required("username"): All(str, Length(min=3)),
            Required("email"): Email(),
            Required("name"): All(str, Length(min=2)),
            Required("password"): All(str, Length(min=6)),
        },
        extra=REMOVE_EXTRA,
    )
)
def signup(username, email, name, password):
    existing_user = get_user_from_username_or_email(username=username, email=email)
    if existing_user:
        if existing_user.username == username:
            raise ApiException("This username is taken", status_codes.HTTP_409_CONFLICT)
        elif existing_user.email == email:
            raise ApiException("This email is already being used by another account", status_codes.HTTP_409_CONFLICT)
    user = User.create_user(username=username, email=email, name=name, password=password)
    db.session.add(user)
    db.session.commit()
    # FIXME db transaction fail 5xx error Flask global exception
    return "", status_codes.HTTP_204_NO_CONTENT
