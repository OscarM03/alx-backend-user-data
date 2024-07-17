#!/usr/bin/env python3
"""auth module"""

import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hash the password using bcrypt"""
    bytes_pwd = password.encode("utf-8")
    hashed_pwd = bcrypt.hashpw(bytes_pwd, bcrypt.gensalt())

    return hashed_pwd


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        "New instance"
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user"""
        user = self._db._session.query(User).filter_by(email=email).first()
        if user:
            raise ValueError(f"User {email} already exists")
        else:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
        return new_user
