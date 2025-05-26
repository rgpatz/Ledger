from sqlalchemy.orm import Session
from . import models, schemas

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