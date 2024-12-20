#!/usr/bin/env python3
"""Auth module
"""

import bcrypt
import uuid
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


def _generate_uuid() -> str:
    """Function to Generate UUIDs"""
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """Method that handles credentials validation

        Args:
            email (str): email of user
            password (str): password of user

        Return: boolean
            True: If entered credentials are valid
            False: If entered credentials are invalid
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """Method that generates a new UUID
           and store it in the database as the user’s session id

        Args:
            email (str): email of the user to generate a session id for
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return

        user.session_id = _generate_uuid()
        return user.session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """Method to find user by session ID

        Args:
            session_id (str): session ID to use in query

        Return:
             the corresponding User or None if not found
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return

        if user:
            return user

    def destroy_session(self, user_id: int) -> None:
        """Method to destroy a sessionby deleting the session ID

        Args:
            user_id (int): user ID for user to destroy session for
        """
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return

        if user:
            user.session_id = None

    def get_reset_password_token(self, email: str) -> str:
        """Method to find user corresponding to the email and
            generate a token to aid password reset

        Args:
            email (str): email of user to search for
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        token = _generate_uuid()
        user.reset_token = token
        self._db._session.commit()
        return token

    def update_password(self, reset_token: str, password: str) -> None:
        """Method to find user corresponding to the email and
           update the password

        Args:
            reset_token (str): token to authenticate reset
            password (str): new password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        hash_pwd = _hash_password(password)
        self._db.update_user(
                user.id,
                hashed_password=hash_pwd,
                reset_token=None
        )
