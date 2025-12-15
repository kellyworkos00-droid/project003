from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from app.db import SessionLocal
from app.models.deal import Deal
from app.fastapi_auth import require_auth

router = APIRouter()


def get_session():
    return SessionLocal()


@router.get("/")
async def list_deals(_: dict = Depends(require_auth)):
    with get_session() as db:
        rows = db.execute(select(Deal).order_by(Deal.id.desc())).scalars().all()
        return [
            {
                "id": d.id,
                "title": d.title,
                "amount": float(d.amount) if d.amount is not None else 0.0,
                "stage": d.stage,
                "contact_id": d.contact_id,
            }
            for d in rows
        ]


@router.post("/")
async def create_deal(payload: dict, _: dict = Depends(require_auth)):
    title = payload.get("title")
    if not title:
        raise HTTPException(status_code=400, detail="title is required")

    d = Deal(
        title=title,
        amount=payload.get("amount", 0),
        stage=payload.get("stage"),
        contact_id=payload.get("contact_id"),
    )
    with get_session() as db:
        db.add(d)
        db.commit()
        db.refresh(d)
        return {
            "id": d.id,
            "title": d.title,
            "amount": float(d.amount) if d.amount is not None else 0.0,
            "stage": d.stage,
            "contact_id": d.contact_id,
        }
