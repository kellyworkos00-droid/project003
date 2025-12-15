from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from app.db import SessionLocal
from app.models.project import Project, Task
from app.fastapi_auth import require_auth

router = APIRouter()


def get_session():
    return SessionLocal()


@router.get("/")
async def list_projects(_: dict = Depends(require_auth)):
    with get_session() as db:
        rows = db.execute(select(Project).order_by(Project.id.desc())).scalars().all()
        return [
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
        ]


@router.post("/")
async def create_project(payload: dict, _: dict = Depends(require_auth)):
    name = payload.get("name")
    code = payload.get("code")
    if not name or not code:
        raise HTTPException(status_code=400, detail="name and code are required")

    p = Project(
        name=name,
        code=code,
        description=payload.get("description"),
        contact_id=payload.get("contact_id"),
        status=payload.get("status", "active"),
        start_date=payload.get("start_date"),
        end_date=payload.get("end_date"),
    )
    with get_session() as db:
        db.add(p)
        db.commit()
        db.refresh(p)
        return {
            "id": p.id,
            "name": p.name,
            "code": p.code,
            "status": p.status,
        }


@router.get("/{project_id}")
async def get_project(project_id: int, _: dict = Depends(require_auth)):
    with get_session() as db:
        p = db.get(Project, project_id)
        if not p:
            raise HTTPException(status_code=404, detail="Project not found")
        return {
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
            ],
        }


@router.get("/{project_id}/tasks")
async def list_tasks(project_id: int, _: dict = Depends(require_auth)):
    with get_session() as db:
        rows = db.execute(select(Task).where(Task.project_id == project_id).order_by(Task.id.desc())).scalars().all()
        return [
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
        ]


@router.post("/{project_id}/tasks")
async def create_task(project_id: int, payload: dict, _: dict = Depends(require_auth)):
    title = payload.get("title")
    if not title:
        raise HTTPException(status_code=400, detail="title is required")

    t = Task(
        project_id=project_id,
        title=title,
        description=payload.get("description"),
        assigned_to_id=payload.get("assigned_to_id"),
        status=payload.get("status", "todo"),
        priority=payload.get("priority", "medium"),
        due_date=payload.get("due_date"),
    )
    with get_session() as db:
        db.add(t)
        db.commit()
        db.refresh(t)
        return {
            "id": t.id,
            "project_id": t.project_id,
            "title": t.title,
            "status": t.status,
        }


@router.delete("/{project_id}")
async def delete_project(project_id: int, _: dict = Depends(require_auth)):
    with get_session() as db:
        p = db.get(Project, project_id)
        if not p:
            raise HTTPException(status_code=404, detail="Project not found")
        db.delete(p)
        db.commit()
        return {"ok": True}
