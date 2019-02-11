from flask import jsonify

from .status_codes import HTTP_400_BAD_REQUEST


class ApiException(Exception):
    def __init__(self, message, status=HTTP_400_BAD_REQUEST, payload=None):
        super()
        self.message = message
        self.status = status
        self.payload = payload

    def to_response(self):
        return jsonify({"message": self.message, "payload": self.payload}), self.status
