#!/usr/bin/env python3
"""
End-to-end integration test
"""

import requests

BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """Integration test for POST /users endpoint (register user)
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
    """Integration test for POST /sessions endpoint (login with wrong password)
    """
    response = requests.post(
            f"{BASE_URL}/sessions",
            data={"email": email, "password": password})

    status_code = response.status_code

    assert status_code == 401, f"Expected 401, got {status_code}"


def log_in(email: str, password: str) -> str:
    """Integration test for POST /sessions endpoint (valid login)
    """
    response = requests.post(
            f"{BASE_URL}/sessions",
            data={"email": email, "password": password})

    expected_response = {"email": email, "message": "logged in"}

    data = response.json()
    status_code = response.status_code

    assert data == expected_response, f"Unexpected response: {data}"
    assert status_code == 200, f"Expected 200, got {status_code}"
    assert "session_id" in response.cookies

    return response.cookies["session_id"]


def profile_unlogged() -> None:
    """Integration test for GET /profile endpoint (without logging in)
    """
    response = requests.get(f"{BASE_URL}/profile")

    status_code = response.status_code

    assert status_code == 403, f"Expected 403, got {status_code}"


def profile_logged(session_id: str) -> None:
    """Integration test for GET /profile endpoint (after logging in)
    """
    headers = {"Cookie": f"session_id={session_id}"}
    response = requests.get(f"{BASE_URL}/profile", headers=headers)

    data = response.json()
    status_code = response.status_code

    assert status_code == 200, f"Expected 200, got {status_code}"
    assert "email" in data


def log_out(session_id: str) -> None:
    """Integration test for DELETE /sessions endpoint (log out)
    """
    headers = {"Cookie": f"session_id={session_id}"}
    response = requests.delete(
            f"{BASE_URL}/sessions", headers=headers, allow_redirects=False)

    status_code = response.status_code

    assert status_code == 302, f"Expected 302, got {status_code}"

    redirect_location = response.headers.get("Location")
    assert redirect_location == f"{BASE_URL}/",\
        f"Expected redirect to {BASE_URL}, got {redirect_location}"

    response = requests.get(redirect_location)
    data = response.json()
    status_code = response.status_code

    expected_response = {"message": "Bienvenue"}

    assert data == expected_response, f"Unexpected response: {data}"
    assert status_code == 200, f"Expected 200, got {status_code}"


def reset_password_token(email: str) -> str:
    """Integration test for POST /reset_password endpoint (get reset token)
    """
    data = {"email": email}
    response = requests.post(f"{BASE_URL}/reset_password", data=data)
    data = response.json()
    status_code = response.status_code

    assert "reset_token" in data
    assert status_code == 200, f"Expected 200, got {status_code}"

    return data["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Integration test for PUT /reset_password endpoint (get reset token)
    """
    data = {"email": email,
            "reset_token": reset_token,
            "new_password": new_password}
    response = requests.put(f"{BASE_URL}/reset_password", data=data)

    data = response.json()
    status_code = response.status_code

    expected_response = {"email": email, "message": "Password updated"}

    assert data == expected_response, f"Unexpected response: {data}"
    assert status_code == 200, f"Expected 200, got {status_code}"


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
