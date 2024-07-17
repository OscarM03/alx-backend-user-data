#!/usr/bin/env python3
"""auth module"""

import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hash the password using bcrypt"""
    bytes_pwd = password.encode("utf-8")
    hashed_pwd = bcrypt.hashpw(bytes_pwd, bcrypt.gensalt())

    return hashed_pwd


def _generate_uuid() -> str:
    """generates uuid"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        "Initialize a new instance of Auth"
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """Validate password"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        bytes_pwd = password.encode("utf-8")
        return bcrypt.checkpw(bytes_pwd, user.hashed_password)

    def create_session(self, email: str) -> str:
        """Creating a session_id"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Returns user or None if not found"""
        if not session_id:
            return None

        user = self._db.find_user_by(session_id=session_id)
        if not user:
            return None
        return user
