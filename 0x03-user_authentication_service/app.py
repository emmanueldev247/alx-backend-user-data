#!/usr/bin/env python3
"""Flask app
"""
from auth import Auth
from flask import abort, Flask, jsonify, request

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
