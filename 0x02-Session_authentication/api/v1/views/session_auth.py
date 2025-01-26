
#!/usr/bin/env python3
"""
Module of Sesson auth views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os


@app_views.route(
    '/auth_session/login',
    methods=['POST'],
    strict_slashes=False
)
def login():
    """
    Logs in a user by validating the email and password
    provided in the request form.

    Returns:
        A JSON response containing the user information if
        the login is successful. Otherwise, returns an error
        JSON response with the appropriate status code.
    """
    email = request.form.get('email', None)
    passwd = request.form.get('password', None)
    if not email or not email.strip():
        return jsonify({"error": "email missing"}), 400
    elif not passwd or not passwd.strip():
        return jsonify({"error": "password missing"}), 400

    user = User.search({"email": email})

    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    elif not user[0].is_valid_password(passwd):
        return jsonify({"error": "wrong password"}), 401
    else:
        from api.v1.app import auth
        user = user[0]
        session_id = auth.create_session(user.id)

        response = jsonify(user.to_json())
        response.set_cookie(os.getenv('SESSION_NAME'), session_id)
        return response


@app_views.route(
    '/auth_session/logout',
    methods=['DELETE'],
    strict_slashes=False
)
def logout():
    """
    Log out the user by destroying the session.

    Returns:
        A tuple containing an empty JSON response
        and a status code of 200 if the session is
        successfully destroyed. Otherwise, it aborts
        with a status code of 404.
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
