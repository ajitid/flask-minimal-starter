from flask import request
from voluptuous import Invalid

from .exceptions import ApiException


def dataschema(schema):
    # Armin Ronacher - Flask for fun and profit - conf video - 29:00
    def decorator(request_handler):
        def call_request_handler(*args, **kwargs):
            try:
                json = None
                try:
                    json = request.get_json()
                except Exception:
                    raise ApiException(f"JSON not supplied")
                kwargs.update(schema(json))
            except Invalid as e:
                path = ".".join(map(lambda item: str(item), e.path))
                raise ApiException(f'Invalid data: {e.msg} (path "{path}")')
            return request_handler(*args, **kwargs)

        return call_request_handler

    return decorator
