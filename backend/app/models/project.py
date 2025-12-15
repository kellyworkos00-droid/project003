from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Date, Text
from sqlalchemy.orm import relationship
from app.db import Base


class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    contact_id = Column(Integer, ForeignKey("contact.id"), nullable=True, index=True)
    status = Column(String(50), nullable=False, default="active")  # active, on_hold, completed, cancelled
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    contact = relationship("Contact", backref="projects")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("project.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    assigned_to_id = Column(Integer, ForeignKey("user.id"), nullable=True, index=True)
    status = Column(String(50), nullable=False, default="todo")  # todo, in_progress, review, done
    priority = Column(String(20), nullable=False, default="medium")  # low, medium, high, urgent
    due_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    project = relationship("Project", back_populates="tasks")
    assigned_to = relationship("User", backref="tasks")
    time_sheets = relationship("TimeSheet", back_populates="task", cascade="all, delete-orphan")


class TimeSheet(Base):
    __tablename__ = "time_sheet"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("task.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    hours = Column(Integer, nullable=False)  # Store in minutes for precision, display as hours
    description = Column(String(500), nullable=True)
    date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    task = relationship("Task", back_populates="time_sheets")
    user = relationship("User", backref="time_sheets")
