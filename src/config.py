import os

basedir = os.path.dirname(__file__)
rootdir = os.path.dirname(basedir)


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URI") or "sqlite:///" + os.path.join(rootdir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # probably needed for sessions (cookies), drop if not needed anymore ->
    SECRET_KEY = os.environ.get("SECRET_KEY")
