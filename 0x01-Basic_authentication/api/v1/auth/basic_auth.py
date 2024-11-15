#!/usr/bin/env python3

"""Auth class"""

from api.v1.auth.auth import Auth
import base64


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
