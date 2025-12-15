from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, func
from sqlalchemy.orm import relationship
from app.db import Base

class Department(Base):
    __tablename__ = "department"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

class Employee(Base):
    __tablename__ = "employee"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True, index=True)
    department_id = Column(Integer, ForeignKey("department.id"), nullable=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(320), nullable=True)
    title = Column(String(100), nullable=True)
    manager_id = Column(Integer, ForeignKey("employee.id"), nullable=True)
    hire_date = Column(Date, nullable=True)
    user = relationship("User")
    department = relationship("Department")
    manager = relationship("Employee", remote_side=[id])

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employee.id"), nullable=False, index=True)
    date = Column(Date, nullable=False)
    check_in = Column(DateTime(timezone=True), nullable=True)
    check_out = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    employee = relationship("Employee")

class LeaveRequest(Base):
    __tablename__ = "leave_request"
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employee.id"), nullable=False, index=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    type = Column(String(50), nullable=False)  # vacation, sick, personal
    status = Column(String(50), nullable=False, default="pending")  # pending, approved, rejected
    reason = Column(String(300), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    employee = relationship("Employee")
