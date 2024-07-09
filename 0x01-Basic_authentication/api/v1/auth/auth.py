#!/usr/bin/env python3
"""Auth module"""

from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determine if the path requires authentication.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): A list of paths that do
            not require authentication.

        Returns:
            bool: False for now.
        """
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        if not path.endswith('/'):
            path += '/'

        for ex_path in excluded_paths:
            if ex_path == path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieve the Authorization header from the request.

        Args:
            request: The Flask request object.

        Returns:
            str: None for now.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieve the current user from the request.

        Args:
            request: The Flask request object.

        Returns:
            TypeVar('User'): None for now.
        """
        return None
