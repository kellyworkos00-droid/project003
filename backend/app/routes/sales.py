from flask import Blueprint, request, jsonify, abort
from sqlalchemy import select
from app.db import SessionLocal
from app.models.sale_order import SaleOrder, OrderItem


sales_bp = Blueprint("sales", __name__)


def get_session():
    return SessionLocal()


@sales_bp.get("/")
def list_orders():
    with get_session() as db:
        rows = db.execute(select(SaleOrder).order_by(SaleOrder.id.desc())).scalars().all()
        return jsonify([
            {
                "id": o.id,
                "order_number": o.order_number,
                "contact_id": o.contact_id,
                "status": o.status,
                "total": float(o.total) if o.total is not None else 0.0,
            }
            for o in rows
        ])


@sales_bp.post("/")
def create_order():
    data = request.get_json(force=True) or {}
    order_number = data.get("order_number")
    if not order_number:
        abort(400, description="order_number is required")

    o = SaleOrder(
        order_number=order_number,
        contact_id=data.get("contact_id"),
        status=data.get("status", "draft"),
        total=data.get("total", 0),
    )
    with get_session() as db:
        db.add(o)
        db.commit()
        db.refresh(o)
        return jsonify({
            "id": o.id,
            "order_number": o.order_number,
            "contact_id": o.contact_id,
            "status": o.status,
            "total": float(o.total) if o.total is not None else 0.0,
        }), 201


@sales_bp.get("/<int:order_id>")
def get_order(order_id: int):
    with get_session() as db:
        o = db.get(SaleOrder, order_id)
        if not o:
            abort(404, description="Order not found")
        return jsonify({
            "id": o.id,
            "order_number": o.order_number,
            "contact_id": o.contact_id,
            "status": o.status,
            "total": float(o.total) if o.total is not None else 0.0,
            "items": [
                {
                    "id": item.id,
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "unit_price": float(item.unit_price) if item.unit_price is not None else 0.0,
                    "subtotal": float(item.subtotal) if item.subtotal is not None else 0.0,
                }
                for item in o.items
            ]
        })


@sales_bp.put("/<int:order_id>")
def update_order(order_id: int):
    data = request.get_json(force=True) or {}
    with get_session() as db:
        o = db.get(SaleOrder, order_id)
        if not o:
            abort(404, description="Order not found")
        for key in ("order_number", "contact_id", "status", "total"):
            if key in data:
                setattr(o, key, data[key])
        db.add(o)
        db.commit()
        db.refresh(o)
        return jsonify({
            "id": o.id,
            "order_number": o.order_number,
            "contact_id": o.contact_id,
            "status": o.status,
            "total": float(o.total) if o.total is not None else 0.0,
        })


@sales_bp.delete("/<int:order_id>")
def delete_order(order_id: int):
    with get_session() as db:
        o = db.get(SaleOrder, order_id)
        if not o:
            abort(404, description="Order not found")
        db.delete(o)
        db.commit()
        return ("", 204)
