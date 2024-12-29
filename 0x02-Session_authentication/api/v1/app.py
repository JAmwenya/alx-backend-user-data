#!/usr/bin/env python3
"""API entry point"""

from flask import Flask, jsonify, request, abort
from os import getenv
from api.v1.views import app_views
from flask_cors import CORS
from api.v1.auth.session_auth import SessionAuth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
if getenv("AUTH_TYPE") == "session_auth":
    auth = SessionAuth()


@app.before_request
def before_request():
    """Handle authentication before each request"""
    if auth is None:
        return
    excluded_paths = [
        "/api/v1/status/",
        "/api/v1/unauthorized/",
        "/api/v1/forbidden/",
        "/api/v1/auth_session/login/",
    ]
    if not auth.require_auth(request.path, excluded_paths):
        return
    if not auth.authorization_header(request) and not auth.session_cookie(request):
        abort(401)
    request.current_user = auth.current_user(request)


@app.errorhandler(404)
def not_found(error):
    """404 Error handler"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
