from flask import jsonify
from flask_login import current_user, login_user, logout_user
from voluptuous import Schema, Required, REMOVE_EXTRA

from app import app
from models.user import User
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


@app.route("/login", methods=["POST"])
@dataschema(Schema({Required("username_or_email"): str, Required("password"): str}, extra=REMOVE_EXTRA))
def login(username_or_email, password):
    user = None
    if is_email(username_or_email):
        user = User.query.filter_by(email=username_or_email).first()
    else:
        user = User.query.filter_by(username=username_or_email).first()
    if user is None or not User.match_password(user, password):
        raise ApiException("Invalid username or password", status_codes.HTTP_401_UNAUTHORIZED)
    login_user(user)
    return "", status_codes.HTTP_204_NO_CONTENT


@app.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return "", status_codes.HTTP_204_NO_CONTENT


@app.route("/")
def protected():
    return "yo"
