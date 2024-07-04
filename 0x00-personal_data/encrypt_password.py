#!/usr/bin/env python3
"""Encrypting passwords"""
import bcrypt


def hash_password(password: str) -> str:
    """returns a salted, hashed password"""
    bytes_pwd = password.encode('utf-8')

    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(bytes_pwd, salt)
    return hashed_pwd
