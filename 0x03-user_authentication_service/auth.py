#!/usr/bin/env python3

"""Authentication Service"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash a password"""
    password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password, salt)
