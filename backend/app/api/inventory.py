from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from app.db import SessionLocal
from app.models.product import Product
from app.fastapi_auth import require_auth

router = APIRouter()


def get_session():
    return SessionLocal()


@router.get("/")
async def list_products(_: dict = Depends(require_auth)):
    with get_session() as db:
        rows = db.execute(select(Product).order_by(Product.id.desc())).scalars().all()
        return [
            {
                "id": p.id,
                "name": p.name,
                "sku": p.sku,
                "description": p.description,
                "price": float(p.price) if p.price is not None else 0.0,
                "stock": p.stock,
            }
            for p in rows
        ]


@router.post("/")
async def create_product(payload: dict, _: dict = Depends(require_auth)):
    name = payload.get("name")
    sku = payload.get("sku")
    if not name or not sku:
        raise HTTPException(status_code=400, detail="name and sku are required")

    p = Product(
        name=name,
        sku=sku,
        description=payload.get("description"),
        price=payload.get("price", 0),
        stock=payload.get("stock", 0),
    )
    with get_session() as db:
        db.add(p)
        db.commit()
        db.refresh(p)
        return {
            "id": p.id,
            "name": p.name,
            "sku": p.sku,
            "description": p.description,
            "price": float(p.price) if p.price is not None else 0.0,
            "stock": p.stock,
        }
