#!/usr/bin/env python3

"""Auth class"""

import base64
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """class to manage the API Basic Authentication"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Method to return the Base64 part of the Authorization header"""
        if not authorization_header or \
           not isinstance(authorization_header, str) or \
           not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split()[1]

    def decode_base64_authorization_header(
                                self, base64_authorization_header: str) -> str:
        """Method that return the decoded value of a Base64 string"""
        if not base64_authorization_header or \
           not isinstance(base64_authorization_header, str):
            return None
        try:
            encoded_bytes = base64_authorization_header.encode('utf-8')
            decoded_bytes = base64.b64decode(encoded_bytes)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Method that returns the user email and
            password from the Base64 decoded value"""
        if not decoded_base64_authorization_header or \
           not isinstance(decoded_base64_authorization_header, str) or \
           ":" not in decoded_base64_authorization_header:
            return None, None
        user_cred = tuple(decoded_base64_authorization_header.split(":", 1))
        if not user_cred or len(user_cred) < 2:
            return None, None
        return user_cred

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Method that returns the User instance
            based on his email and password
        """
        if not user_email or not isinstance(user_email, str) or \
           not user_pwd or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        if not users:
            return None

        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """Method that retrieves the User instance for a request
        """
        auth_header = self.authorization_header(request)
        base64_auth = self.extract_base64_authorization_header(auth_header)
        decoded_auth = self.decode_base64_authorization_header(base64_auth)
        user_email, user_pwd = self.extract_user_credentials(decoded_auth)
        return self.user_object_from_credentials(user_email, user_pwd)
