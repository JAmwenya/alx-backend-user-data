#!/usr/bin/env python3
"""
App entry point for the API.
"""

from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from os import getenv
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
AUTH_TYPE = getenv("AUTH_TYPE", "auth")

if AUTH_TYPE == "basic_auth":
    auth = BasicAuth()
else:
    auth = Auth()


@app.before_request
def before_request():
    """Filter each request before processing."""
    if auth is None:
        return

    excluded_paths = ["/api/v1/status/", "/api/v1/unauthorized/", "/api/v1/forbidden/"]

    if not auth.require_auth(request.path, excluded_paths):
        return

    if auth.authorization_header(request) is None:
        abort(401, description="Unauthorized")

    if auth.current_user(request) is None:
        abort(403, description="Forbidden")


@app.errorhandler(401)
def unauthorized(error):
    """Handler for 401 Unauthorized errors."""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    """Handler for 403 Forbidden errors."""
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error):
    """Handler for 404 Not Found errors."""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = int(getenv("API_PORT", 5000))
    app.run(host=host, port=port)
