#!/usr/bin/env python3

"""Manage the API authentication."""

from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """
    A class to manage authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Define which routes don't need authentication."""
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        if not path.endswith("/"):
            path = path + "/"

        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """Returns authorization header"""
        if request is None or not request.headers.get("Authorization", None):
            return None
        else:
            return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """Manages current user."""

        return None

    def session_cookie(self, request=None):
        """Returns a cookie value from a request"""
        if request is None:
            return None
        session_name = getenv("SESSION_NAME", None)
        if session_name:
            cookie = request.cookies.get(session_name, None)
            return cookie
