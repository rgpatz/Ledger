from sqlalchemy.orm import Session
from . import models, schemas

# Engagement CRUD operations
def get_engagement(db: Session, engagement_id: int):
    return db.query(models.Engagement).filter(models.Engagement.id == engagement_id).first()

def get_engagements(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Engagement).offset(skip).limit(limit).all()

def create_engagement(db: Session, engagement: schemas.EngagementCreate):
    db_engagement = models.Engagement(**engagement.dict())
    db.add(db_engagement)
    db.commit()
    db.refresh(db_engagement)
    return db_engagement

def update_engagement(db: Session, engagement_id: int, engagement_update: schemas.EngagementUpdate):
    db_engagement = get_engagement(db, engagement_id)
    if db_engagement:
        update_data = engagement_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_engagement, key, value)
        db.commit()
        db.refresh(db_engagement)
    return db_engagement

def delete_engagement(db: Session, engagement_id: int):
    db_engagement = get_engagement(db, engagement_id)
    if db_engagement:
        db.delete(db_engagement)
        db.commit()
    return db_engagement

# Client CRUD operations
def get_client(db: Session, client_id: int):
    return db.query(models.Client).filter(models.Client.id == client_id).first()

def get_client_by_name(db: Session, name: str):
    return db.query(models.Client).filter(models.Client.name == name).first()

def get_clients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Client).offset(skip).limit(limit).all()

def create_client(db: Session, client: schemas.ClientCreate):
    # Create client without contacts first
    client_data = client.dict(exclude={'contacts'})
    db_client = models.Client(**client_data)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    
    # Add contacts if provided
    for contact_data in client.contacts:
        db_contact = models.ClientContact(**contact_data.dict(), client_id=db_client.id)
        db.add(db_contact)
    
    db.commit()
    db.refresh(db_client)
    return db_client

def update_client(db: Session, client_id: int, client_update: schemas.ClientUpdate):
    db_client = get_client(db, client_id)
    if db_client:
        update_data = client_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_client, key, value)
        db.commit()
        db.refresh(db_client)
    return db_client

def delete_client(db: Session, client_id: int):
    db_client = get_client(db, client_id)
    if db_client:
        db.delete(db_client)
        db.commit()
    return db_client

# Client Contact CRUD operations
def get_contact(db: Session, contact_id: int):
    return db.query(models.ClientContact).filter(models.ClientContact.id == contact_id).first()

def get_contacts_by_client(db: Session, client_id: int):
    return db.query(models.ClientContact).filter(models.ClientContact.client_id == client_id).all()

def create_contact(db: Session, contact: schemas.ClientContactCreate, client_id: int):
    db_contact = models.ClientContact(**contact.dict(), client_id=client_id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def update_contact(db: Session, contact_id: int, contact_update: schemas.ClientContactUpdate):
    db_contact = get_contact(db, contact_id)
    if db_contact:
        update_data = contact_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int):
    db_contact = get_contact(db, contact_id)
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact 