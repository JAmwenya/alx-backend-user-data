#!/usr/bin/env python3
"""
Index route for the API.
"""

from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status():
    """API status route."""
    return jsonify({"status": "OK"})


@app_views.route("/unauthorized", methods=["GET"], strict_slashes=False)
def unauthorized():
    """Route to trigger a 401 error."""
    abort(401)


@app_views.route("/forbidden", methods=["GET"], strict_slashes=False)
def forbidden():
    """Route to trigger a 403 error."""
    abort(403)
