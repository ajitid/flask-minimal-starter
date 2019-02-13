import os

from app import app

basedir = os.path.dirname(__file__)
rootdir = os.path.dirname(basedir)


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URI") or "sqlite:///" + os.path.join(rootdir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_BLACKLIST_ENABLED = True


def app_warn_for_env_var(env_var, defaulted_to=None, message=""):
    if os.environ.get(env_var) is None:
        app.logger.warn(
            f'`{env_var}` is not defined as environment variable and is defaulted to {defaulted_to}. '
            + message)


if os.environ.get("FLASK_ENV") is "production":
    app_warn_for_env_var('DB_URI', 'SQLite', 'You should rather set a production level database.')

CORS_API_ORIGINS = os.environ.get("CORS_API_ORIGINS") or ""
app_warn_for_env_var('CORS_API_ORIGINS', '""', 'Instead, set it to the site which will request to this endpoint.')
