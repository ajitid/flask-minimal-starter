from flask_login import LoginManager
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
    user = jwt_get_current_user()
    if user:
        return user
    """
    Python 3.8 has walrus operator, which can simplify the code above and add scope to `user`:
    ```
    if user := jwt_get_current_user():
        return user
    ```
    """

    # finally, return None if both methods did not login the user
    return None
