from flask import jsonify
from flask_login import current_user, login_user, logout_user, login_required
from voluptuous import Schema, Required, REMOVE_EXTRA, In
from flask_jwt_extended import create_access_token, get_jwt_identity, get_raw_jwt


from app import app
from models.user import User
from handlers.jwt import jwt_blacklist
from helpers.decorators import dataschema
from helpers import status_codes
from helpers.exceptions import ApiException
from helpers.fns import is_email


@app.route("/")
def index():
    return jsonify({"status": "All set!"})


@app.route("/check-auth")
def check_auth():
    if not current_user.is_authenticated:
        return jsonify({"authenticated": False})
    user = current_user
    return jsonify({"authenticated": True, "username": user.username})


def get_user_from_username_or_email(username_or_email):
    user = None
    if is_email(username_or_email):
        user = User.query.filter_by(email=username_or_email).first()
    else:
        user = User.query.filter_by(username=username_or_email).first()
    return user


@app.route("/login", methods=["POST"])
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
    user = get_user_from_username_or_email(username_or_email)
    if user is None or not User.match_password(user, password):
        raise ApiException("Invalid username or password", status_codes.HTTP_401_UNAUTHORIZED)
    if auth_type == "cookie":
        login_user(user)
        return "", status_codes.HTTP_204_NO_CONTENT
    elif auth_type == "token":
        token = create_access_token(identity=user.id)
        return jsonify({"access_token": token})
    raise ApiException("Authentication failed", status_codes.HTTP_401_UNAUTHORIZED)


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    if get_jwt_identity() is not None:
        jti = get_raw_jwt()["jti"]
        jwt_blacklist.add(jti)
    else:
        logout_user()
    return "", status_codes.HTTP_204_NO_CONTENT


# TODO
@app.route("/protected")
@login_required
def protected():
    return "yo"
