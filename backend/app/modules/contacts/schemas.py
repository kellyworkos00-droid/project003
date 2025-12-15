from pydantic import BaseModel, EmailStr
from typing import Optional


class ContactBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None


class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None


class ContactOut(ContactBase):
    id: int

    class Config:
        from_attributes = True
