"""Authentication helpers.

This module provides simple email/password authentication for the demo app.
It uses `data/users.json` as the user store. For this project the only
allowed user role is `admin`.

Functions return dictionaries with `ok` and `message` keys for robust
error handling in the UI.
"""
from backend.file_handler import read_json, write_json
from utils.constants import USERS_FILE
from typing import Dict


def _load_users():
    return read_json(str(USERS_FILE)) or []


def _save_users(users):
    write_json(str(USERS_FILE), users)


def get_user_by_email(email: str):
    users = _load_users()
    for u in users:
        if u.get("email") == email:
            return u
    return None


def authenticate_user(email: str, password: str) -> Dict:
    """Authenticate by email and password.

    Returns a dict: {"ok": bool, "message": str, "user": dict|None}
    """
    if not email or not password:
        return {"ok": False, "message": "Email and password are required.", "user": None}

    user = get_user_by_email(email)
    if not user:
        return {"ok": False, "message": "User not found.", "user": None}

    # Plain-text password check for demo (replace with hashed check for production)
    if user.get("password") != password:
        return {"ok": False, "message": "Incorrect password.", "user": None}

    if user.get("role") != "admin":
        return {"ok": False, "message": "User is not an admin.", "user": None}

    return {"ok": True, "message": "Authenticated.", "user": user}


# Registration disabled — only pre-registered admins can login
