#!/usr/bin/env python3

"""Auth class"""

from api.v1.auth.auth import Auth
from flask import request
from typing import List, TypeVar


class BasicAuth(Auth):
    """class to manage the API Basic Authentication"""
    pass
