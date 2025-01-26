#!/usr/bin/env python3
"""
class to manage the API authentication.
"""


from flask import request
from typing import List, TypeVar
import os


class Auth:
    """Auth class to manage the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require authentication"""
        if path is None:
            return True
        if not path.endswith("/"):
            path += "/"
        if excluded_paths is None or not excluded_paths:
            return True

        for excluded_path in excluded_paths:
            if excluded_path.endswith("*") and path.startswith(
                excluded_path[:-1]
            ):
                return False
            elif path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Authorization header"""
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user"""
        return None

    def session_cookie(self, request=None):
        """
        Retrieves the session cookie from the request.

        Args:
            request (Request): The request object.

        Returns:
            str: The value of the session cookie, or None
                if the request is None or the session cookie
                is not found.
        """
        if request is None:
            return None

        session = os.environ.get("SESSION_NAME")
        return request.cookies.get(session, None)