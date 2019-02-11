from flask import jsonify, request
from flask_login import current_user
from voluptuous import Schema, Required, REMOVE_EXTRA

from app import app
from utils.decorators import dataschema


@app.route("/")
def index():
    return jsonify({"status": "All set!"})


@app.route("/check-auth")
def check_auth():
    return jsonify({"authenticated": current_user})


@app.route("/login", methods=["POST"])
@dataschema(Schema({Required("why"): str, Required("ho"): str}, extra=REMOVE_EXTRA))
def login(why, ho):
    return jsonify({"ohno": "yesss"})
