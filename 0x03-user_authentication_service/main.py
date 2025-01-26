
#!/usr/bin/env python3
"""
Main file
"""
import requests

BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    url = f"{BASE_URL}/users"
    payload = {"email": email, "password": password}
    response = requests.post(url, data=payload)
    assert response.status_code == 200, "Failed to register user"


def log_in_wrong_password(email: str, password: str) -> None:
    url = f"{BASE_URL}/login"
    payload = {"email": email, "password": password}
    response = requests.post(url, data=payload)
    assert response.status_code == 404, "Logged in with wrong password"


def log_in(email: str, password: str) -> str:
    url = f"{BASE_URL}/sessions"
    payload = {"email": email, "password": password}
    response = requests.post(url, data=payload)
    assert response.status_code == 200, "Failed to log in"
    return response.cookies['session_id']


def profile_unlogged() -> None:
    url = f"{BASE_URL}/profile"
    response = requests.get(url)
    assert response.status_code == 403, "Profile accessible without logging in"


def profile_logged(session_id: str) -> None:
    url = f"{BASE_URL}/profile"
    headers = {"Authorization": f"Bearer {session_id}"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200, "Failed to access profile after logging in"


def log_out(session_id: str) -> None:
    url = f"{BASE_URL}/sessions"
    headers = {"Authorization": f"Bearer {session_id}"}
    response = requests.post(url, headers=headers)
    assert response.status_code == 200, "Failed to log out"


def reset_password_token(email: str) -> str:
    url = f"{BASE_URL}/reset_password_token"
    payload = {"email": email}
    response = requests.post(url, data=payload)
    assert response.status_code == 200, "Failed to get reset password token"
    return response.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    url = f"{BASE_URL}/update_password"
    payload = {"email": email, "reset_token": reset_token,
               "new_password": new_password}
    response = requests.post(url, data=payload)
    assert response.status_code == 200, "Failed to update password"


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    # register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
