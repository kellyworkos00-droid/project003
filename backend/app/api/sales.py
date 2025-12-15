from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from app.db import SessionLocal
from app.models.sale_order import SaleOrder
from app.fastapi_auth import require_auth

router = APIRouter()


def get_session():
    return SessionLocal()


@router.get("/")
async def list_orders(_: dict = Depends(require_auth)):
    with get_session() as db:
        rows = db.execute(select(SaleOrder).order_by(SaleOrder.id.desc())).scalars().all()
        return [
            {
                "id": o.id,
                "order_number": o.order_number,
                "contact_id": o.contact_id,
                "status": o.status,
                "total": float(o.total) if o.total is not None else 0.0,
            }
            for o in rows
        ]


@router.post("/")
async def create_order(payload: dict, _: dict = Depends(require_auth)):
    order_number = payload.get("order_number")
    if not order_number:
        raise HTTPException(status_code=400, detail="order_number is required")

    o = SaleOrder(
        order_number=order_number,
        contact_id=payload.get("contact_id"),
        status=payload.get("status", "draft"),
        total=payload.get("total", 0),
    )
    with get_session() as db:
        db.add(o)
        db.commit()
        db.refresh(o)
        return {
            "id": o.id,
            "order_number": o.order_number,
            "contact_id": o.contact_id,
            "status": o.status,
            "total": float(o.total) if o.total is not None else 0.0,
        }
