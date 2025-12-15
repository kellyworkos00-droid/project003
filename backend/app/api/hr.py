from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from app.db import SessionLocal
from app.fastapi_auth import require_auth
from app.models.hr import Employee, Department, Attendance, LeaveRequest

router = APIRouter()

def get_session():
    return SessionLocal()

# Employees
@router.get("/employees")
async def list_employees(_: dict = Depends(require_auth)):
    with get_session() as db:
        rows = db.execute(select(Employee).order_by(Employee.id.desc())).scalars().all()
        return [
            {
                "id": e.id,
                "first_name": e.first_name,
                "last_name": e.last_name,
                "email": e.email,
                "title": e.title,
                "department_id": e.department_id,
                "manager_id": e.manager_id,
                "hire_date": str(e.hire_date) if e.hire_date else None,
            }
            for e in rows
        ]

@router.post("/employees")
async def create_employee(payload: dict, _: dict = Depends(require_auth)):
    fn = payload.get("first_name"); ln = payload.get("last_name")
    if not fn or not ln:
        raise HTTPException(status_code=400, detail="first_name and last_name required")
    e = Employee(first_name=fn, last_name=ln,
                 email=payload.get("email"), title=payload.get("title"),
                 department_id=payload.get("department_id"), manager_id=payload.get("manager_id"),
                 hire_date=payload.get("hire_date"))
    with get_session() as db:
        db.add(e); db.commit(); db.refresh(e)
        return {"id": e.id}

# Departments
@router.get("/departments")
async def list_departments(_: dict = Depends(require_auth)):
    with get_session() as db:
        rows = db.execute(select(Department).order_by(Department.name)).scalars().all()
        return [{"id": d.id, "name": d.name} for d in rows]

@router.post("/departments")
async def create_department(payload: dict, _: dict = Depends(require_auth)):
    name = payload.get("name")
    if not name:
        raise HTTPException(status_code=400, detail="name required")
    d = Department(name=name)
    with get_session() as db:
        db.add(d); db.commit(); db.refresh(d)
        return {"id": d.id, "name": d.name}

# Attendance
@router.get("/attendance")
async def list_attendance(_: dict = Depends(require_auth)):
    with get_session() as db:
        rows = db.execute(select(Attendance).order_by(Attendance.date.desc())).scalars().all()
        return [{
            "id": a.id,
            "employee_id": a.employee_id,
            "date": str(a.date),
            "check_in": str(a.check_in) if a.check_in else None,
            "check_out": str(a.check_out) if a.check_out else None,
        } for a in rows]

@router.post("/attendance")
async def create_attendance(payload: dict, _: dict = Depends(require_auth)):
    emp_id = payload.get("employee_id"); date = payload.get("date")
    if not emp_id or not date:
        raise HTTPException(status_code=400, detail="employee_id and date required")
    a = Attendance(employee_id=emp_id, date=date, check_in=payload.get("check_in"), check_out=payload.get("check_out"))
    with get_session() as db:
        db.add(a); db.commit(); db.refresh(a)
        return {"id": a.id}

# Leave Requests
@router.get("/leave")
async def list_leave(_: dict = Depends(require_auth)):
    with get_session() as db:
        rows = db.execute(select(LeaveRequest).order_by(LeaveRequest.created_at.desc())).scalars().all()
        return [{
            "id": l.id,
            "employee_id": l.employee_id,
            "start_date": str(l.start_date),
            "end_date": str(l.end_date),
            "type": l.type,
            "status": l.status,
            "reason": l.reason,
        } for l in rows]

@router.post("/leave")
async def create_leave(payload: dict, _: dict = Depends(require_auth)):
    emp_id = payload.get("employee_id"); start = payload.get("start_date"); end = payload.get("end_date"); type_ = payload.get("type")
    if not emp_id or not start or not end or not type_:
        raise HTTPException(status_code=400, detail="employee_id, start_date, end_date, type required")
    l = LeaveRequest(employee_id=emp_id, start_date=start, end_date=end, type=type_, status=payload.get("status", "pending"), reason=payload.get("reason"))
    with get_session() as db:
        db.add(l); db.commit(); db.refresh(l)
        return {"id": l.id}
