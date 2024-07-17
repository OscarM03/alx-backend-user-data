#!/usr/bin/env python3
"""auth module"""

import bcrypt


def _hash_password(passowrd: str) -> bytes:
    """Convert the password to bytes"""
    bytes_pwd = passowrd.encode("utf-8")
    hashed_pwd = bcrypt.hashpw(bytes_pwd, bcrypt.gensalt())

    return hashed_pwd
