from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from app.db import SessionLocal
from app.models.invoice import Invoice
from app.fastapi_auth import require_auth

router = APIRouter()


def get_session():
    return SessionLocal()


@router.get("/")
async def list_invoices(_: dict = Depends(require_auth)):
    with get_session() as db:
        rows = db.execute(select(Invoice).order_by(Invoice.id.desc())).scalars().all()
        return [
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
        ]


@router.post("/")
async def create_invoice(payload: dict, _: dict = Depends(require_auth)):
    invoice_number = payload.get("invoice_number")
    if not invoice_number:
        raise HTTPException(status_code=400, detail="invoice_number is required")

    inv = Invoice(
        invoice_number=invoice_number,
        sale_order_id=payload.get("sale_order_id"),
        contact_id=payload.get("contact_id"),
        status=payload.get("status", "draft"),
        invoice_date=payload.get("invoice_date"),
        due_date=payload.get("due_date"),
        subtotal=payload.get("subtotal", 0),
        tax=payload.get("tax", 0),
        total=payload.get("total", 0),
        notes=payload.get("notes"),
    )
    with get_session() as db:
        db.add(inv)
        db.commit()
        db.refresh(inv)
        return {
            "id": inv.id,
            "invoice_number": inv.invoice_number,
            "sale_order_id": inv.sale_order_id,
            "contact_id": inv.contact_id,
            "status": inv.status,
            "total": float(inv.total) if inv.total is not None else 0.0,
        }


@router.get("/{invoice_id}")
async def get_invoice(invoice_id: int, _: dict = Depends(require_auth)):
    with get_session() as db:
        inv = db.get(Invoice, invoice_id)
        if not inv:
            raise HTTPException(status_code=404, detail="Invoice not found")
        return {
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
            ],
        }


@router.put("/{invoice_id}")
async def update_invoice(invoice_id: int, payload: dict, _: dict = Depends(require_auth)):
    with get_session() as db:
        inv = db.get(Invoice, invoice_id)
        if not inv:
            raise HTTPException(status_code=404, detail="Invoice not found")
        for key in (
            "invoice_number",
            "sale_order_id",
            "contact_id",
            "status",
            "invoice_date",
            "due_date",
            "subtotal",
            "tax",
            "total",
            "notes",
        ):
            if key in payload:
                setattr(inv, key, payload[key])
        db.add(inv)
        db.commit()
        db.refresh(inv)
        return {
            "id": inv.id,
            "invoice_number": inv.invoice_number,
            "status": inv.status,
            "total": float(inv.total) if inv.total is not None else 0.0,
        }


@router.delete("/{invoice_id}")
async def delete_invoice(invoice_id: int, _: dict = Depends(require_auth)):
    with get_session() as db:
        inv = db.get(Invoice, invoice_id)
        if not inv:
            raise HTTPException(status_code=404, detail="Invoice not found")
        db.delete(inv)
        db.commit()
        return {"ok": True}
