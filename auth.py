from __future__ import annotations

import hashlib
import json
import os
import secrets

import paths
USERS_PATH = paths.writable("users.json")

DEFAULT_ADMIN_USER = "admin"
DEFAULT_ADMIN_PASS = "admin123"

ROLES = ("admin", "user")


class User:
    def __init__(self, username: str, display_name: str, role: str):
        self.username = username
        self.display_name = display_name or username
        self.role = role if role in ROLES else "user"


def _hash_password(password: str, salt_hex: str) -> str:
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"),
                                 bytes.fromhex(salt_hex), 200_000)
    return digest.hex()


def load_users() -> dict:
    try:
        with open(USERS_PATH, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return {}


def save_users(users: dict) -> None:
    os.makedirs(os.path.dirname(USERS_PATH), exist_ok=True)
    tmp = USERS_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(users, fh, indent=2)
    os.replace(tmp, USERS_PATH)


def ensure_default_admin() -> bool:
    """Create the default admin account if it does not exist.

    Returns True when the account was freshly created (first run)."""
    users = load_users()
    if DEFAULT_ADMIN_USER in users:
        return False
    salt = secrets.token_hex(16)
    users[DEFAULT_ADMIN_USER] = {
        "display_name": "Administrator",
        "role": "admin",
        "salt": salt,
        "hash": _hash_password(DEFAULT_ADMIN_PASS, salt),
    }
    save_users(users)
    return True


def authenticate(username: str, password: str) -> User | None:
    users = load_users()
    entry = users.get((username or "").strip().lower())
    if not entry:
        return None
    if _hash_password(password or "", entry["salt"]) != entry["hash"]:
        return None
    return User(entry_key(username), entry.get("display_name", ""),
                entry.get("role", "user"))


def entry_key(username: str) -> str:
    return (username or "").strip().lower()


def create_user(username: str, password: str, display_name: str,
                role: str = "user") -> tuple[User | None, str]:
    """Returns (user, error_code); error_code '' on success."""
    key = entry_key(username)
    if not key or not password:
        return None, "err_fill"
    users = load_users()
    if key in users:
        return None, "err_taken"
    salt = secrets.token_hex(16)
    users[key] = {
        "display_name": (display_name or "").strip() or key,
        "role": role if role in ROLES else "user",
        "salt": salt,
        "hash": _hash_password(password, salt),
    }
    save_users(users)
    return User(key, users[key]["display_name"], users[key]["role"]), ""
