from flask import Blueprint, request, jsonify, abort
from sqlalchemy import select
from app.db import SessionLocal
from app.models.deal import Deal
from app.auth import require_auth


deals_bp = Blueprint("deals", __name__)


def get_session():
    return SessionLocal()


@deals_bp.get("/")
@require_auth
def list_deals():
    with get_session() as db:
        rows = db.execute(select(Deal).order_by(Deal.id.desc())).scalars().all()
        return jsonify([
            {
                "id": d.id,
                "title": d.title,
                "amount": float(d.amount) if d.amount is not None else 0.0,
                "stage": d.stage,
                "contact_id": d.contact_id,
            }
            for d in rows
        ])


@deals_bp.post("/")
@require_auth
def create_deal():
    data = request.get_json(force=True) or {}
    title = data.get("title")
    if not title:
        abort(400, description="title is required")

    d = Deal(
        title=title,
        amount=data.get("amount", 0),
        stage=data.get("stage"),
        contact_id=data.get("contact_id"),
    )
    with get_session() as db:
        db.add(d)
        db.commit()
        db.refresh(d)
        return jsonify({
            "id": d.id,
            "title": d.title,
            "amount": float(d.amount) if d.amount is not None else 0.0,
            "stage": d.stage,
            "contact_id": d.contact_id,
        }), 201


@deals_bp.get("/<int:deal_id>")
def get_deal(deal_id: int):
    with get_session() as db:
        d = db.get(Deal, deal_id)
        if not d:
            abort(404, description="Deal not found")
        return jsonify({
            "id": d.id,
            "title": d.title,
            "amount": float(d.amount) if d.amount is not None else 0.0,
            "stage": d.stage,
            "contact_id": d.contact_id,
        })


@deals_bp.put("/<int:deal_id>")
def update_deal(deal_id: int):
    data = request.get_json(force=True) or {}
    with get_session() as db:
        d = db.get(Deal, deal_id)
        if not d:
            abort(404, description="Deal not found")
        for key in ("title", "amount", "stage", "contact_id"):
            if key in data:
                setattr(d, key, data[key])
        db.add(d)
        db.commit()
        db.refresh(d)
        return jsonify({
            "id": d.id,
            "title": d.title,
            "amount": float(d.amount) if d.amount is not None else 0.0,
            "stage": d.stage,
            "contact_id": d.contact_id,
        })


@deals_bp.delete("/<int:deal_id>")
def delete_deal(deal_id: int):
    with get_session() as db:
        d = db.get(Deal, deal_id)
        if not d:
            abort(404, description="Deal not found")
        db.delete(d)
        db.commit()
        return ("", 204)
