from flask import Blueprint, request, jsonify, abort
from sqlalchemy import select
from app.db import SessionLocal
from app.models.invoice import Invoice, InvoiceItem
from app.auth import require_auth

invoices_bp = Blueprint("invoices", __name__)


def get_session():
    return SessionLocal()


@invoices_bp.get("/")
@require_auth
def list_invoices():
    with get_session() as db:
        rows = db.execute(select(Invoice).order_by(Invoice.id.desc())).scalars().all()
        return jsonify([
            {
                "id": inv.id,
                "invoice_number": inv.invoice_number,
                "sale_order_id": inv.sale_order_id,
                "contact_id": inv.contact_id,
                "status": inv.status,
                "invoice_date": str(inv.invoice_date) if inv.invoice_date else None,
                "due_date": str(inv.due_date) if inv.due_date else None,
                "total": float(inv.total) if inv.total is not None else 0.0,
            }
            for inv in rows
        ])


@invoices_bp.post("/")
@require_auth
def create_invoice():
    data = request.get_json(force=True) or {}
    invoice_number = data.get("invoice_number")
    if not invoice_number:
        abort(400, description="invoice_number is required")

    inv = Invoice(
        invoice_number=invoice_number,
        sale_order_id=data.get("sale_order_id"),
        contact_id=data.get("contact_id"),
        status=data.get("status", "draft"),
        invoice_date=data.get("invoice_date"),
        due_date=data.get("due_date"),
        subtotal=data.get("subtotal", 0),
        tax=data.get("tax", 0),
        total=data.get("total", 0),
        notes=data.get("notes"),
    )
    with get_session() as db:
        db.add(inv)
        db.commit()
        db.refresh(inv)
        return jsonify({
            "id": inv.id,
            "invoice_number": inv.invoice_number,
            "sale_order_id": inv.sale_order_id,
            "contact_id": inv.contact_id,
            "status": inv.status,
            "total": float(inv.total) if inv.total is not None else 0.0,
        }), 201


@invoices_bp.get("/<int:invoice_id>")
@require_auth
def get_invoice(invoice_id: int):
    with get_session() as db:
        inv = db.get(Invoice, invoice_id)
        if not inv:
            abort(404, description="Invoice not found")
        return jsonify({
            "id": inv.id,
            "invoice_number": inv.invoice_number,
            "sale_order_id": inv.sale_order_id,
            "contact_id": inv.contact_id,
            "status": inv.status,
            "invoice_date": str(inv.invoice_date) if inv.invoice_date else None,
            "due_date": str(inv.due_date) if inv.due_date else None,
            "subtotal": float(inv.subtotal) if inv.subtotal is not None else 0.0,
            "tax": float(inv.tax) if inv.tax is not None else 0.0,
            "total": float(inv.total) if inv.total is not None else 0.0,
            "notes": inv.notes,
            "items": [
                {
                    "id": item.id,
                    "product_id": item.product_id,
                    "description": item.description,
                    "quantity": item.quantity,
                    "unit_price": float(item.unit_price) if item.unit_price is not None else 0.0,
                    "subtotal": float(item.subtotal) if item.subtotal is not None else 0.0,
                }
                for item in inv.items
            ]
        })


@invoices_bp.put("/<int:invoice_id>")
@require_auth
def update_invoice(invoice_id: int):
    data = request.get_json(force=True) or {}
    with get_session() as db:
        inv = db.get(Invoice, invoice_id)
        if not inv:
            abort(404, description="Invoice not found")
        for key in ("invoice_number", "sale_order_id", "contact_id", "status", "invoice_date", 
                    "due_date", "subtotal", "tax", "total", "notes"):
            if key in data:
                setattr(inv, key, data[key])
        db.add(inv)
        db.commit()
        db.refresh(inv)
        return jsonify({
            "id": inv.id,
            "invoice_number": inv.invoice_number,
            "status": inv.status,
            "total": float(inv.total) if inv.total is not None else 0.0,
        })


@invoices_bp.delete("/<int:invoice_id>")
@require_auth
def delete_invoice(invoice_id: int):
    with get_session() as db:
        inv = db.get(Invoice, invoice_id)
        if not inv:
            abort(404, description="Invoice not found")
        db.delete(inv)
        db.commit()
        return ("", 204)
