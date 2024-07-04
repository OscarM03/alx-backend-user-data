#!/usr/bin/env python3
"""Encrypting passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted, hashed password"""
    bytes_pwd = password.encode('utf-8')
    hashed_pwd = bcrypt.hashpw(bytes_pwd, bcrypt.gensalt())
    return hashed_pwd
