#!/usr/bin/env python3

"""Auth class"""

from api.v1.auth.auth import Auth
from flask import request
from typing import List, TypeVar


class BasicAuth(Auth):
    """class to manage the API Basic Authentication"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Method to return the Base64 part of the Authorization header"""
        if not authorization_header or \
           not isinstance(authorization_header, str) or \
           not authorization_header.startswith("Basic "):
            return authorization_header.split()[1]
