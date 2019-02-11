import os

basedir = os.path.dirname(__file__)
rootdir = os.path.dirname(basedir)


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URI") or "sqlite:///" + os.path.join(rootdir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_BLACKLIST_ENABLED = True
