from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas, models
from app.database import get_db

router = APIRouter(
    prefix="/api/v1/clients",
    tags=["clients"],
)

# Client endpoints
@router.post("/", response_model=schemas.ClientRead, status_code=status.HTTP_201_CREATED)
def create_new_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    # Check if client name already exists
    existing_client = crud.get_client_by_name(db, name=client.name)
    if existing_client:
        raise HTTPException(status_code=400, detail="Client with this name already exists")
    return crud.create_client(db=db, client=client)

@router.get("/", response_model=List[schemas.ClientRead])
def read_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clients = crud.get_clients(db, skip=skip, limit=limit)
    return clients

@router.get("/{client_id}", response_model=schemas.ClientRead)
def read_client(client_id: int, db: Session = Depends(get_db)):
    db_client = crud.get_client(db, client_id=client_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client

@router.put("/{client_id}", response_model=schemas.ClientRead)
def update_existing_client(client_id: int, client_update: schemas.ClientUpdate, db: Session = Depends(get_db)):
    db_client = crud.update_client(db, client_id=client_id, client_update=client_update)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client

@router.delete("/{client_id}", response_model=schemas.ClientRead)
def delete_existing_client(client_id: int, db: Session = Depends(get_db)):
    db_client = crud.delete_client(db, client_id=client_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client

# Client Contact endpoints
@router.post("/{client_id}/contacts", response_model=schemas.ClientContactRead, status_code=status.HTTP_201_CREATED)
def create_new_contact(client_id: int, contact: schemas.ClientContactCreate, db: Session = Depends(get_db)):
    # Verify client exists
    db_client = crud.get_client(db, client_id=client_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return crud.create_contact(db=db, contact=contact, client_id=client_id)

@router.get("/{client_id}/contacts", response_model=List[schemas.ClientContactRead])
def read_client_contacts(client_id: int, db: Session = Depends(get_db)):
    # Verify client exists
    db_client = crud.get_client(db, client_id=client_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    contacts = crud.get_contacts_by_client(db, client_id=client_id)
    return contacts

@router.get("/{client_id}/contacts/{contact_id}", response_model=schemas.ClientContactRead)
def read_contact(client_id: int, contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.get_contact(db, contact_id=contact_id)
    if db_contact is None or db_contact.client_id != client_id:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.put("/{client_id}/contacts/{contact_id}", response_model=schemas.ClientContactRead)
def update_existing_contact(client_id: int, contact_id: int, contact_update: schemas.ClientContactUpdate, db: Session = Depends(get_db)):
    db_contact = crud.get_contact(db, contact_id=contact_id)
    if db_contact is None or db_contact.client_id != client_id:
        raise HTTPException(status_code=404, detail="Contact not found")
    db_contact = crud.update_contact(db, contact_id=contact_id, contact_update=contact_update)
    return db_contact

@router.delete("/{client_id}/contacts/{contact_id}", response_model=schemas.ClientContactRead)
def delete_existing_contact(client_id: int, contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.get_contact(db, contact_id=contact_id)
    if db_contact is None or db_contact.client_id != client_id:
        raise HTTPException(status_code=404, detail="Contact not found")
    db_contact = crud.delete_contact(db, contact_id=contact_id)
    return db_contact 