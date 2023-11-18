#!/usr/bin/env python3

"""Authentication Service"""
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from db import DB
from user import User
import bcrypt
import uuid


def _hash_password(password: str) -> bytes:
    """Hash a password"""
    password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password, salt)


def _generate_uuid() -> str:
    """Generate uuid"""
    return str(uuid.uuid4())


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

        hashed_password = _hash_password(password).decode('utf-8')
        self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """Validate a login"""
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                hashed_password = user.hashed_password.encode('utf-8')
                user_password = password.encode('utf-8')
                if bcrypt.checkpw(user_password, hashed_password):
                    return True
                else:
                    return False
        except (NoResultFound, InvalidRequestError):
            return False

    def create_session(self, email: str) -> [str, None]:
        """Create a new session"""
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                session_id = _generate_uuid()
                self._db.update_user(user_id=user.id, session_id=session_id)
                return session_id
        except (NoResultFound, InvalidRequestError):
            return None
