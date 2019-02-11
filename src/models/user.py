from datetime import datetime
from uuid import uuid4
from flask_login import UserMixin
import bcrypt

from handlers.db import db


def get_uuid():
    return str(uuid4())


class User(UserMixin, db.Model):
    id = db.Column(db.String(64), primary_key=True, default=get_uuid)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    hashed_password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, encoded_password):
        self.hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())

    @staticmethod
    def match_password(user, password_to_check):
        return bcrypt.checkpw(password_to_check.encode("utf-8"), user.hashed_password)

    @classmethod
    def create_user(cls, username, email, name, password):
        user = cls(username=username, name=name, email=email)
        user.set_password(password.encode("utf-8"))
        return user

    def __repr__(self):
        return f"<User {self.username}>"
