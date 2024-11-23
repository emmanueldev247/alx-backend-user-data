#!/usr/bin/env python3
"""Auth module
"""

import bcrypt
from user import User
from db import DB
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Function to hash password

    Args:
        password (str): password string to hash

    Return: Salted hash of the input password
    """
    salt = bcrypt.gensalt()
    encoded_pwd = password.encode('utf-8')
    return bcrypt.hashpw(encoded_pwd, salt)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Method to register a new user

        Args:
            email (str): email of user
            password (str): password of user

        Return: A User object

        Raises:
            ValueError: If a user already exist with the passed email
        """
        try:
            user_check = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hash_pwd = _hash_password(password)

            user = self._db.add_user(email, hash_pwd)
            return user
