from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas, models
from app.database import get_db

router = APIRouter(
    prefix="/api/v1/engagements",
    tags=["engagements"],
)

@router.post("/", response_model=schemas.EngagementRead, status_code=status.HTTP_201_CREATED)
def create_new_engagement(engagement: schemas.EngagementCreate, db: Session = Depends(get_db)):
    return crud.create_engagement(db=db, engagement=engagement)

@router.get("/", response_model=List[schemas.EngagementRead])
def read_engagements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    engagements = crud.get_engagements(db, skip=skip, limit=limit)
    return engagements

@router.get("/{engagement_id}", response_model=schemas.EngagementRead)
def read_engagement(engagement_id: int, db: Session = Depends(get_db)):
    db_engagement = crud.get_engagement(db, engagement_id=engagement_id)
    if db_engagement is None:
        raise HTTPException(status_code=404, detail="Engagement not found")
    return db_engagement

@router.put("/{engagement_id}", response_model=schemas.EngagementRead)
def update_existing_engagement(engagement_id: int, engagement_update: schemas.EngagementUpdate, db: Session = Depends(get_db)):
    db_engagement = crud.update_engagement(db, engagement_id=engagement_id, engagement_update=engagement_update)
    if db_engagement is None:
        raise HTTPException(status_code=404, detail="Engagement not found")
    return db_engagement

@router.delete("/{engagement_id}", response_model=schemas.EngagementRead) 
def delete_existing_engagement(engagement_id: int, db: Session = Depends(get_db)):
    db_engagement = crud.delete_engagement(db, engagement_id=engagement_id)
    if db_engagement is None: 
        raise HTTPException(status_code=404, detail="Engagement not found")
    return db_engagement  