#!/usr/bin/env python3

"""Manage the API authentication."""

from flask import request
from typing import List, TypeVar


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
        """Manages authorization"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Manages current user."""

        return None
