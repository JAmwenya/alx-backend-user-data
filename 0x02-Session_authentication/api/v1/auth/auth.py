#!/usr/bin/env python3
"""Auth module"""

import os


class Auth:
    """Base Auth class"""

    def session_cookie(self, request=None):
        """Returns a cookie value from a request"""
        if request is None:
            return None
        session_name = os.getenv("SESSION_NAME", "_my_session_id")
        return request.cookies.get(session_name)
