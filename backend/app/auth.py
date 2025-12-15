import os
from flask import Blueprint, request, jsonify, current_app
from itsdangerous import TimestampSigner, BadSignature, SignatureExpired

auth_bp = Blueprint("auth", __name__)


def _signer() -> TimestampSigner:
    secret = current_app.config.get("SECRET_KEY") or os.getenv("SECRET_KEY", "dev-secret")
    return TimestampSigner(secret_key=secret)


@auth_bp.post("/login")
def login():
    data = request.get_json(force=True) or {}
    username = data.get("username")
    password = data.get("password")

    expected_u = os.getenv("ADMIN_USERNAME", "admin")
    expected_p = os.getenv("ADMIN_PASSWORD", "admin")

    if username == expected_u and password == expected_p:
        token = _signer().sign(username.encode()).decode()
        return jsonify({"token": token})
    return jsonify({"error": "invalid credentials"}), 401


def verify_token(token: str) -> bool:
    try:
        _signer().unsign(token, max_age=60 * 60 * 24)  # 24h
        return True
    except (BadSignature, SignatureExpired):
        return False
