#!/usr/bin/env python3
"""Flask app
"""
from auth import Auth
from flask import abort, Flask, jsonify, request, redirect

AUTH = Auth()
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def home():
    """route handler for "/"
    """
    return jsonify({"message": "Bienvenue"}), 200


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """route handler for "/users"
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if not (email and password):
        abort(400)
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """route handler for POST "/sessions"
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if not (email and password):
        abort(400)

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)

    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)

    return response, 200


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """route handler for DELETE "/sessions"
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if not (user and session_id):
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """route handler for GET "/profile"
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if not (user and session_id):
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """route handler for POST "/reset_password"
    """
    email = request.form.get("email")
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """route handler for PUT "/reset_password"
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    if not (email and reset_token and new_password):
        abort(403)
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
