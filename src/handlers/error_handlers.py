from app import app
from helpers.exceptions import ApiException

app.register_error_handler(ApiException, lambda err: err.to_response())
