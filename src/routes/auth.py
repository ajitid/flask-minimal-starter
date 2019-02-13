from flask import jsonify, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from voluptuous import Schema, Required, REMOVE_EXTRA, In, All, Length, Email
from flask_jwt_extended import create_access_token, get_jwt_identity, get_raw_jwt
from sqlalchemy import or_

from models.user import User
from handlers.db import db
from handlers.jwt import jwt_blacklist
from helpers.decorators import dataschema
from helpers import status_codes
from helpers.exceptions import ApiException
from helpers.fns import is_email

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
        login_user(user)
        return "", status_codes.HTTP_204_NO_CONTENT
    elif auth_type is "token":
        token = create_access_token(identity=user.id)
        return jsonify({"access_token": token})
    raise ApiException("Authentication failed", status_codes.HTTP_401_UNAUTHORIZED)


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
            Required("username"): All(str, Length(min=4)),
            Required("email"): Email(),
            Required("name"): All(str, Length(min=1)),
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
