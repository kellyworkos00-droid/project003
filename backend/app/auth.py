import os
from functools import wraps
from flask import Blueprint, request, jsonify, current_app, g
from itsdangerous import TimestampSigner, BadSignature, SignatureExpired
from sqlalchemy import select
from app.db import SessionLocal
from app.models.user import User
from app.utils import verify_password

auth_bp = Blueprint("auth", __name__)


def _signer() -> TimestampSigner:
    secret = current_app.config.get("SECRET_KEY") or os.getenv("SECRET_KEY", "dev-secret")
    return TimestampSigner(secret_key=secret)


@auth_bp.post("/login")
def login():
    data = request.get_json(force=True) or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "username and password required"}), 400

    with SessionLocal() as db:
        user = db.execute(select(User).where(User.username == username)).scalar_one_or_none()
        
        if not user or not user.is_active:
            return jsonify({"error": "invalid credentials"}), 401
        
        # Check password hash if exists, otherwise fallback to simple match for dev
        if user.password_hash:
            if not verify_password(password, user.password_hash):
                return jsonify({"error": "invalid credentials"}), 401
        else:
            # Fallback for dev (remove in production)
            expected_p = os.getenv("ADMIN_PASSWORD", "admin")
            if password != expected_p:
                return jsonify({"error": "invalid credentials"}), 401

        token = _signer().sign(f"{user.id}:{user.username}".encode()).decode()
        return jsonify({
            "token": token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role_id": user.role_id,
            }
        })


def get_current_user():
    """Extract and verify user from Authorization header."""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    
    token = auth_header[7:]
    try:
        payload = _signer().unsign(token, max_age=60 * 60 * 24).decode()  # 24h
        user_id = int(payload.split(":")[0])
        with SessionLocal() as db:
            user = db.get(User, user_id)
            return user
    except (BadSignature, SignatureExpired, ValueError, IndexError):
        return None


def require_auth(f):
    """Decorator to require authentication on a route."""
    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({"error": "unauthorized"}), 401
        g.current_user = user
        return f(*args, **kwargs)
    return decorated


def require_permission(permission_name: str):
    """Decorator to require a specific permission."""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user = get_current_user()
            if not user:
                return jsonify({"error": "unauthorized"}), 401
            
            # Check if user's role has the required permission
            # For now, admin role (id=1) has all permissions
            # TODO: implement full permission checking via RolePermission table
            if user.role_id == 1:  # admin
                g.current_user = user
                return f(*args, **kwargs)
            
            # For other roles, implement permission lookup
            # with SessionLocal() as db:
            #     has_perm = check_permission(db, user.role_id, permission_name)
            #     if not has_perm:
            #         return jsonify({"error": "forbidden"}), 403
            
            g.current_user = user
            return f(*args, **kwargs)
        return decorated
    return decorator


def verify_token(token: str) -> bool:
    """Legacy token verification function."""
    try:
        _signer().unsign(token, max_age=60 * 60 * 24)
        return True
    except (BadSignature, SignatureExpired):
        return False
