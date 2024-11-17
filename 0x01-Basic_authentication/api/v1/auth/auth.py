#!/usr/bin/env python3

"""Auth class"""

from flask import request
from typing import List, TypeVar


class Auth:
    """class to manage the API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """public method"""
        if not path or not excluded_paths or len(excluded_paths) == 0:
            return True

        if path[-1] != '/':
            path += '/'

        for ex_path in excluded_paths:
            if ex_path[-1] == "*":
                ex_path = ex_path[:-1]
            if path.startswith(ex_path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """public method"""
        if not request or "Authorization" not in request.headers:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """public method"""
        return None
