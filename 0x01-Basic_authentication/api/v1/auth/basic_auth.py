#!/usr/bin/env python3

"""Manage the Basic authentication"""

from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User
import uuid


class BasicAuth(Auth):
    """A class to manage basic authentication"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Returns header part"""
        if (authorization_header is None or type(authorization_header) is not
                str or not authorization_header.startswith("Basic ")):
            return None
        return authorization_header.split()[1]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """returns the decoded value of a Base64 string"""

        try:
            header = base64.b64decode(base64_authorization_header)
            return header.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """
        returns the user email and password from the Base64 decoded value
        """
        try:
            credentials = decoded_base64_authorization_header.split(":")
            return credentials[0], credentials[1]
        except Exception:
            return None, None

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """returns the User instance based on his email and password."""
        if (type(user_pwd), type(user_email)) != (str, str):
            return None

        try:
            users = User.search({"email": user_email})
        except Exception:
            return None
        if len(users) > 0:
            if users[0].is_valid_password(user_pwd):
                return users[0]

        return None
