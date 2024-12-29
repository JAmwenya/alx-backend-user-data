#!/usr/bin/env python3
"""
User model for database operations.
"""

from models.base import Base
import bcrypt


class User(Base):
    """User class for managing user data."""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a User instance."""
        super().__init__(*args, **kwargs)
        self.email = kwargs.get("email")
        self.password = kwargs.get("password")

    def is_valid_password(self, pwd: str) -> bool:
        """Check if a password is valid."""
        if not pwd or not self.password:
            return False
        return bcrypt.checkpw(pwd.encode("utf-8"), self.password.encode("utf-8"))
