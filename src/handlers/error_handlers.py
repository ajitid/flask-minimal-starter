from app import app
from helpers.exceptions import ApiException
from helpers.status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

app.register_error_handler(ApiException, lambda err: err.to_response())


@app.errorhandler(HTTP_404_NOT_FOUND)
def not_found(err):
    return "", HTTP_404_NOT_FOUND


@app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
def internal_server_error(err):
    # TODO report to error logger, emailer
    return "", HTTP_500_INTERNAL_SERVER_ERROR
