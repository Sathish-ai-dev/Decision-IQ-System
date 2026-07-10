from __future__ import annotations

from bcrypt import gensalt, hashpw, checkpw


DEFAULT_BCRYPT_ROUNDS = 12


def hash_password(password: str, *, rounds: int = DEFAULT_BCRYPT_ROUNDS) -> str:
    """Hash a plaintext password with bcrypt."""

    if not password:
        raise ValueError("Password cannot be empty.")

    password_bytes = password.encode("utf-8")
    hashed = hashpw(password_bytes, gensalt(rounds)).decode("utf-8")
    return hashed


def verify_password(password: str, password_hash: str) -> bool:
    """Return True when the plaintext password matches the stored hash."""

    if not password or not password_hash:
        return False

    try:
        return checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except ValueError:
        return False
