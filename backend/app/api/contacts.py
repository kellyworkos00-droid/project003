from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from app.db import SessionLocal
from app.models.contact import Contact
from app.fastapi_auth import require_auth

router = APIRouter()


def get_session():
    return SessionLocal()


@router.get("/")
async def list_contacts(_: dict = Depends(require_auth)):
    with get_session() as db:
        rows = db.execute(select(Contact).order_by(Contact.id.desc())).scalars().all()
        return [
            {
                "id": c.id,
                "name": c.name,
                "email": c.email,
                "phone": c.phone,
                "company": c.company,
            }
            for c in rows
        ]


@router.post("/")
async def create_contact(payload: dict, _: dict = Depends(require_auth)):
    name = payload.get("name")
    if not name:
        raise HTTPException(status_code=400, detail="name is required")

    c = Contact(
        name=name,
        email=payload.get("email"),
        phone=payload.get("phone"),
        company=payload.get("company"),
    )
    with get_session() as db:
        db.add(c)
        db.commit()
        db.refresh(c)
        return {
            "id": c.id,
            "name": c.name,
            "email": c.email,
            "phone": c.phone,
            "company": c.company,
        }
