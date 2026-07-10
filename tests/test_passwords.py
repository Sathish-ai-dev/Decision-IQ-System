from __future__ import annotations

import pytest

from app.core.passwords import hash_password, verify_password


def test_hash_password_returns_bcrypt_hash() -> None:
    hashed = hash_password("correct horse battery staple", rounds=4)

    assert hashed.startswith("$2")
    assert verify_password("correct horse battery staple", hashed) is True


def test_verify_password_rejects_wrong_password() -> None:
    hashed = hash_password("correct horse battery staple", rounds=4)

    assert verify_password("wrong password", hashed) is False


def test_hash_password_rejects_empty_password() -> None:
    with pytest.raises(ValueError, match="Password cannot be empty."):
        hash_password("")
