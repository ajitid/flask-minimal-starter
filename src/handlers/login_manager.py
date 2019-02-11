from flask import g
from flask.sessions import SecureCookieSessionInterface
from flask_login import LoginManager, user_loaded_from_header
from flask_jwt_extended import jwt_optional, get_current_user as jwt_get_current_user

from app import app
from models.user import User
from helpers import status_codes
from helpers.exceptions import ApiException

login_manager = LoginManager(app)


@login_manager.user_loader
def user_loader(id):
    return User.query.get(id)


@login_manager.unauthorized_handler
def unauthorized():
    raise ApiException("Not authenticated or authorized", status_codes.HTTP_401_UNAUTHORIZED)


class CustomSessionInterface(SecureCookieSessionInterface):
    """Prevent creating session from API requests."""

    def save_session(self, *args, **kwargs):
        if g.get("login_via_header"):
            return
        return super(CustomSessionInterface, self).save_session(*args, **kwargs)


app.session_interface = CustomSessionInterface()


@user_loaded_from_header.connect
def user_loaded_from_header(self, user=None):
    g.login_via_header = True


@login_manager.request_loader
@jwt_optional
def load_user_from_request(request):

    """
    # first, try to login using the api_key url arg
    api_key = request.args.get("api_key")
    if api_key:
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user
    """

    # next, try to return user from JWT
    # FIXME on fail, JWT lib gives back {"msg": "..."} and not {"message": "..."}
    user = jwt_get_current_user()
    if user:
        return user

    # finally, return None if both methods did not login the user
    return None
