#!/usr/bin/env python3
"""
End-to-end integration test
"""

import requests


BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """Integration test for register user
    """
    response = requests.post(
            f"{BASE_URL}/users",
            data={"email": email, "password": password})

    expected_response = {"email": email, "message": "user created"}

    data = response.json()
    status_code = response.status_code

    assert data == expected_response, f"Unexpected response: {data}"
    assert status_code == 200, f"Expected 200, got {status_code}"


def log_in_wrong_password(email: str, password: str) -> None:
    """Integration test for log in with wrong password
    """
    response = requests.post(
            f"{BASE_URL}/sessions",
            data={"email": email, "password": password})

    status_code = response.status_code

    assert status_code == 401, f"Expected 401, got {status_code}"


def log_in(email: str, password: str) -> str:
    """Integration test for valid log in
    """
    response = requests.post(
            f"{BASE_URL}/sessions",
            data={"email": email, "password": password})

    expected_response = {"email": email, "message": "logged in"}

    data = response.json()
    status_code = response.status_code

    assert data == expected_response, f"Unexpected response: {data}"
    assert status_code == 200, f"Expected 200, got {status_code}"
    assert "session_id" in data

    return data["session_id"]


def profile_unlogged() -> None:
    """Integration test for profile GET without logging in
    """
    response = requests.get(f"{BASE_URL}/profile")
    status_code = response.status_code
    assert status_code == 403, f"Expected 403, got {status_code}"



EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
