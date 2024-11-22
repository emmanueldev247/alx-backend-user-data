#!/usr/bin/env python3
"""Auth module
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """Function to hash password

    Args:
        password (str): password string to hash

    Return: Salted hash of the input password
    """
    salt = bcrypt.gensalt()
    encoded_pwd = password.encode('utf-8')
    return bcrypt.hashpw(encoded_pwd, salt)
