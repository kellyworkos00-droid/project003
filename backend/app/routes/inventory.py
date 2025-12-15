from flask import Blueprint, request, jsonify, abort
from sqlalchemy import select
from app.db import SessionLocal
from app.models.product import Product
from app.auth import require_auth


inventory_bp = Blueprint("inventory", __name__)


def get_session():
    return SessionLocal()


@inventory_bp.get("/")
@require_auth
def list_products():
    with get_session() as db:
        rows = db.execute(select(Product).order_by(Product.id.desc())).scalars().all()
        return jsonify([
            {
                "id": p.id,
                "name": p.name,
                "sku": p.sku,
                "description": p.description,
                "price": float(p.price) if p.price is not None else 0.0,
                "stock": p.stock,
            }
            for p in rows
        ])


@inventory_bp.post("/")
@require_auth
def create_product():
    data = request.get_json(force=True) or {}
    name = data.get("name")
    sku = data.get("sku")
    if not name or not sku:
        abort(400, description="name and sku are required")

    p = Product(
        name=name,
        sku=sku,
        description=data.get("description"),
        price=data.get("price", 0),
        stock=data.get("stock", 0),
    )
    with get_session() as db:
        db.add(p)
        db.commit()
        db.refresh(p)
        return jsonify({
            "id": p.id,
            "name": p.name,
            "sku": p.sku,
            "description": p.description,
            "price": float(p.price) if p.price is not None else 0.0,
            "stock": p.stock,
        }), 201


@inventory_bp.get("/<int:product_id>")
def get_product(product_id: int):
    with get_session() as db:
        p = db.get(Product, product_id)
        if not p:
            abort(404, description="Product not found")
        return jsonify({
            "id": p.id,
            "name": p.name,
            "sku": p.sku,
            "description": p.description,
            "price": float(p.price) if p.price is not None else 0.0,
            "stock": p.stock,
        })


@inventory_bp.put("/<int:product_id>")
def update_product(product_id: int):
    data = request.get_json(force=True) or {}
    with get_session() as db:
        p = db.get(Product, product_id)
        if not p:
            abort(404, description="Product not found")
        for key in ("name", "sku", "description", "price", "stock"):
            if key in data:
                setattr(p, key, data[key])
        db.add(p)
        db.commit()
        db.refresh(p)
        return jsonify({
            "id": p.id,
            "name": p.name,
            "sku": p.sku,
            "description": p.description,
            "price": float(p.price) if p.price is not None else 0.0,
            "stock": p.stock,
        })


@inventory_bp.delete("/<int:product_id>")
def delete_product(product_id: int):
    with get_session() as db:
        p = db.get(Product, product_id)
        if not p:
            abort(404, description="Product not found")
        db.delete(p)
        db.commit()
        return ("", 204)
