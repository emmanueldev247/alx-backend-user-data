#!/usr/bin/env python3

"""Auth class"""

from flask import request
from typing import List, TypeVar


class Auth:
    """class to manage the API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """public method"""
        return False

    def authorization_header(self, request=None) -> str:
        """public method"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """public method"""
        return None