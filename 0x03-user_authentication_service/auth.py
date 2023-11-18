#!/usr/bin/env python3

"""Authentication Service"""
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from db import DB
from user import User
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash a password"""
    password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password, salt)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user"""
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except (NoResultFound, InvalidRequestError):
            pass
        if user is not None:
            raise ValueError("User {} already exists".format(email))

        hashed_password = str(_hash_password(password))
        self._db.add_user(email, hashed_password)
