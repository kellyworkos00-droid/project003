from flask import Blueprint, request, jsonify, abort
from sqlalchemy import select
from app.db import SessionLocal
from app.models.contact import Contact

contacts_bp = Blueprint("contacts", __name__)


def get_session():
    return SessionLocal()


@contacts_bp.get("/")
def list_contacts():
    with get_session() as db:
        rows = db.execute(select(Contact).order_by(Contact.id.desc())).scalars().all()
        return jsonify([
            {
                "id": c.id,
                "name": c.name,
                "email": c.email,
                "phone": c.phone,
                "company": c.company,
            }
            for c in rows
        ])


@contacts_bp.post("/")
def create_contact():
    data = request.get_json(force=True) or {}
    name = data.get("name")
    if not name:
        abort(400, description="name is required")

    c = Contact(
        name=name,
        email=data.get("email"),
        phone=data.get("phone"),
        company=data.get("company"),
    )
    with get_session() as db:
        db.add(c)
        db.commit()
        db.refresh(c)
        return jsonify({
            "id": c.id,
            "name": c.name,
            "email": c.email,
            "phone": c.phone,
            "company": c.company,
        }), 201


@contacts_bp.get("/<int:contact_id>")
def get_contact(contact_id: int):
    with get_session() as db:
        c = db.get(Contact, contact_id)
        if not c:
            abort(404, description="Contact not found")
        return jsonify({
            "id": c.id,
            "name": c.name,
            "email": c.email,
            "phone": c.phone,
            "company": c.company,
        })


@contacts_bp.put("/<int:contact_id>")
def update_contact(contact_id: int):
    data = request.get_json(force=True) or {}
    with get_session() as db:
        c = db.get(Contact, contact_id)
        if not c:
            abort(404, description="Contact not found")
        for key in ("name", "email", "phone", "company"):
            if key in data:
                setattr(c, key, data[key])
        db.add(c)
        db.commit()
        db.refresh(c)
        return jsonify({
            "id": c.id,
            "name": c.name,
            "email": c.email,
            "phone": c.phone,
            "company": c.company,
        })


@contacts_bp.delete("/<int:contact_id>")
def delete_contact(contact_id: int):
    with get_session() as db:
        c = db.get(Contact, contact_id)
        if not c:
            abort(404, description="Contact not found")
        db.delete(c)
        db.commit()
        return ("", 204)
