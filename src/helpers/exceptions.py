from flask import jsonify

from .status_codes import HTTP_400_BAD_REQUEST


class ApiException(Exception):
    def __init__(self, msg, status=HTTP_400_BAD_REQUEST, payload=None):
        super()
        self.msg = msg
        self.status = status
        self.payload = payload

    def to_response(self):
        return jsonify({"msg": self.msg, "payload": self.payload}), self.status
