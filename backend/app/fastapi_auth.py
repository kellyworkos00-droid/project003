import os
from typing import Optional, Callable
from fastapi import APIRouter, Depends, Header, HTTPException, status
from itsdangerous import TimestampSigner, BadSignature, SignatureExpired
from sqlalchemy import select
from app.db import SessionLocal
from app.models.user import User
from app.utils import verify_password

router = APIRouter()


def _signer() -> TimestampSigner:
    secret = os.getenv("SECRET_KEY", "dev-secret")
    return TimestampSigner(secret_key=secret)


@router.post("/login")
async def login(payload: dict):
    username = payload.get("username")
    password = payload.get("password")
    if not username or not password:
        raise HTTPException(status_code=400, detail="username and password required")

    with SessionLocal() as db:
        user = db.execute(select(User).where(User.username == username)).scalar_one_or_none()
        if not user or not user.is_active:
            raise HTTPException(status_code=401, detail="invalid credentials")

        if user.password_hash:
            if not verify_password(password, user.password_hash):
                raise HTTPException(status_code=401, detail="invalid credentials")
        else:
            expected_p = os.getenv("ADMIN_PASSWORD", "admin")
            if password != expected_p:
                raise HTTPException(status_code=401, detail="invalid credentials")

        token = _signer().sign(f"{user.id}:{user.username}".encode()).decode()
        return {
            "token": token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role_id": user.role_id,
            },
        }


async def get_current_user(Authorization: Optional[str] = Header(default=None)) -> Optional[User]:
    if not Authorization or not Authorization.startswith("Bearer "):
        return None
    token = Authorization[7:]
    try:
        payload = _signer().unsign(token, max_age=60 * 60 * 24).decode()
        user_id = int(payload.split(":")[0])
        with SessionLocal() as db:
            user = db.get(User, user_id)
            return user
    except (BadSignature, SignatureExpired, ValueError, IndexError):
        return None


async def require_auth(user: Optional[User] = Depends(get_current_user)) -> User:
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized")
    return user


def require_permission(permission_name: str) -> Callable:
    async def dependency(user: User = Depends(require_auth)) -> User:
        # Admin shortcut
        if user.role_id == 1:
            return user
        # TODO: implement proper RolePermission lookup
        return user
    return dependency
