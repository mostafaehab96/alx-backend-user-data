#!/usr/bin/env python3
""" Module of Session views
"""
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from os import getenv
from models.user import User


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login_user() -> str:
    """
    If every thing is successfull
    :return: User instance and json representation
    """
    email = request.form.get("email", None)
    password = request.form.get("password", None)
    if email is None:
        return jsonify({"error": "email missing"}), 400
    if password is None:
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})
    if users is None or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    response = make_response(user.to_json())
    session_name = getenv("SESSION_NAME")
    response.set_cookie(session_name, session_id)
    return response


@app_views.route("auth_session/logout", methods=["DELETE"],
                 strict_slashes=False)
def delete_session() -> str:
    """
    Deletes the current session
    :return: empty json
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
