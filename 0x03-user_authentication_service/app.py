#!/usr/bin/env python3
"""Basic Authentication Service"""

from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', strict_slashes=False)
def index():
    """Index page"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """Creates a new user"""
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": f"{email}", "message": "user created"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
