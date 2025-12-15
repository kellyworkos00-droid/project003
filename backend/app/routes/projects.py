from flask import Blueprint, request, jsonify, abort
from sqlalchemy import select
from app.db import SessionLocal
from app.models.project import Project, Task, TimeSheet
from app.auth import require_auth

projects_bp = Blueprint("projects", __name__)


def get_session():
    return SessionLocal()


@projects_bp.get("/")
@require_auth
def list_projects():
    with get_session() as db:
        rows = db.execute(select(Project).order_by(Project.id.desc())).scalars().all()
        return jsonify([
            {
                "id": p.id,
                "name": p.name,
                "code": p.code,
                "status": p.status,
                "contact_id": p.contact_id,
                "start_date": str(p.start_date) if p.start_date else None,
                "end_date": str(p.end_date) if p.end_date else None,
            }
            for p in rows
        ])


@projects_bp.post("/")
@require_auth
def create_project():
    data = request.get_json(force=True) or {}
    name = data.get("name")
    code = data.get("code")
    if not name or not code:
        abort(400, description="name and code are required")

    p = Project(
        name=name,
        code=code,
        description=data.get("description"),
        contact_id=data.get("contact_id"),
        status=data.get("status", "active"),
        start_date=data.get("start_date"),
        end_date=data.get("end_date"),
    )
    with get_session() as db:
        db.add(p)
        db.commit()
        db.refresh(p)
        return jsonify({
            "id": p.id,
            "name": p.name,
            "code": p.code,
            "status": p.status,
        }), 201


@projects_bp.get("/<int:project_id>")
@require_auth
def get_project(project_id: int):
    with get_session() as db:
        p = db.get(Project, project_id)
        if not p:
            abort(404, description="Project not found")
        return jsonify({
            "id": p.id,
            "name": p.name,
            "code": p.code,
            "description": p.description,
            "contact_id": p.contact_id,
            "status": p.status,
            "start_date": str(p.start_date) if p.start_date else None,
            "end_date": str(p.end_date) if p.end_date else None,
            "tasks": [
                {
                    "id": t.id,
                    "title": t.title,
                    "status": t.status,
                    "priority": t.priority,
                    "assigned_to_id": t.assigned_to_id,
                    "due_date": str(t.due_date) if t.due_date else None,
                }
                for t in p.tasks
            ]
        })


# Task endpoints
@projects_bp.get("/<int:project_id>/tasks")
@require_auth
def list_tasks(project_id: int):
    with get_session() as db:
        rows = db.execute(select(Task).where(Task.project_id == project_id).order_by(Task.id.desc())).scalars().all()
        return jsonify([
            {
                "id": t.id,
                "project_id": t.project_id,
                "title": t.title,
                "status": t.status,
                "priority": t.priority,
                "assigned_to_id": t.assigned_to_id,
                "due_date": str(t.due_date) if t.due_date else None,
            }
            for t in rows
        ])


@projects_bp.post("/<int:project_id>/tasks")
@require_auth
def create_task(project_id: int):
    data = request.get_json(force=True) or {}
    title = data.get("title")
    if not title:
        abort(400, description="title is required")

    t = Task(
        project_id=project_id,
        title=title,
        description=data.get("description"),
        assigned_to_id=data.get("assigned_to_id"),
        status=data.get("status", "todo"),
        priority=data.get("priority", "medium"),
        due_date=data.get("due_date"),
    )
    with get_session() as db:
        db.add(t)
        db.commit()
        db.refresh(t)
        return jsonify({
            "id": t.id,
            "project_id": t.project_id,
            "title": t.title,
            "status": t.status,
        }), 201


@projects_bp.delete("/<int:project_id>")
@require_auth
def delete_project(project_id: int):
    with get_session() as db:
        p = db.get(Project, project_id)
        if not p:
            abort(404, description="Project not found")
        db.delete(p)
        db.commit()
        return ("", 204)
