from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.modules.contacts import schemas
from app.modules.contacts.models import Contact

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=List[schemas.ContactOut])
def list_contacts(db: Session = Depends(get_db)):
    return db.query(Contact).order_by(Contact.id.desc()).all()


@router.post("/", response_model=schemas.ContactOut, status_code=status.HTTP_201_CREATED)
def create_contact(payload: schemas.ContactCreate, db: Session = Depends(get_db)):
    contact = Contact(**payload.model_dump())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


@router.get("/{contact_id}", response_model=schemas.ContactOut)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put("/{contact_id}", response_model=schemas.ContactOut)
def update_contact(contact_id: int, payload: schemas.ContactUpdate, db: Session = Depends(get_db)):
    contact = db.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(contact, k, v)

    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return None
