#!/usr/bin/env python3
"""
Password encryption and validation module.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt.
    Args:
        password (str): Plaintext password.
    Returns:
        bytes: Hashed password.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validate a password against its hashed version.
    Args:
        hashed_password (bytes): Hashed password.
        password (str): Plaintext password to validate.
    Returns:
        bool: True if valid, False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
