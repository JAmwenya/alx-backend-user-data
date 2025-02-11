#!/usr/bin/env python3
"""
Auth class for API authentication.
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """Template for all authentication methods."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if the path requires authentication."""
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        if path[-1] != "/":
            path += "/"

        for excluded_path in excluded_paths:
            if excluded_path.endswith("*") and path.startswith(excluded_path[:-1]):
                return False
            if path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Return the Authorization header from the request."""
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar("User"):
        """Return the current user."""
        return None
