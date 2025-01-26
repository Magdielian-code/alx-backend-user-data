
#!/usr/bin/env python3
"""
Basic Flask app
"""


from flask import Flask, jsonify, request, abort, make_response, redirect, url_for
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def welcome():
    """
    Returns a JSON response with a welcome message.

    :return: JSON response with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """
    Register a new user.

    This function handles the registration of a new user by
    extracting the email and password from the request form.
    It then calls the `register_user` method of the `AUTH`
    object to register the user. If the registration is successful,
    it returns a JSON response with the user's email and a success
    message. If the email is already registered, it returns a JSON
    response with an error message.

    Returns:
      A JSON response containing the user's email and a success
      message if the registration is successful.
      A JSON response with an error message if the email is already
      registered.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        new_user = AUTH.register_user(email, password)
        return jsonify({"email": new_user.email,
                        "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> make_response:
    """
    Logs in a user by validating the provided email and password.

    Returns:
        A response object with a JSON payload containing the user's
        email and a success message.

    Raises:
        HTTPException: If the provided email and password are invalid.
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    res_data = {"email": email, "message": "logged in"}

    response = make_response(jsonify(res_data), 200)
    response.set_cookie('session_id', session_id)
    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> make_response:
    """
    Logs out a user by deleting the session cookie.

    Returns:
        A response object with a JSON payload containing a success message.

    Raises:
        HTTPException: If the session cookie is not set.
    """
    session_id = request.cookies.get("session_id")
    try:
        user = AUTH.get_user_from_session_id(session_id)
        if not user:
            abort(403)
        AUTH.destroy_session(user.id)
        return redirect(url_for("welcome"))
    except:
        abort(403)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> make_response:
    """Rturens a JSON response with the user's email."""
    session_id = request.cookies.get("session_id")
    try:
        user = AUTH.get_user_from_session_id(session_id)
        if not user:
            abort(403)
        return jsonify({"email": user.email}), 200
    except:
        abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> make_response:
    email = request.form.get("email")
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> make_response:
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
