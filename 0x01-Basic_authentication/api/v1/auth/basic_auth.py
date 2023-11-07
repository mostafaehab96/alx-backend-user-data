#!/usr/bin/env python3

"""Manage the Basic authentication"""

from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """A class to manage basic authentication"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Returns encoded header with base64"""
        if (authorization_header is None or type(authorization_header) is not
                str or not authorization_header.startswith("Basic ")):
            return None
        return authorization_header.split()[1]
