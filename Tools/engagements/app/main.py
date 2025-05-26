from fastapi import FastAPI, Depends, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles # If you add CSS/JS
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import create_db_and_tables, get_db
from app.routers import engagement_api
from app import crud, schemas, models # app refers to the 'app' directory
from app.models import EngagementStatus # Import the enum
from datetime import date
from typing import Optional

# Create database tables on startup, Alembic will be used later, need to figure out how to do this in a production environment. Needs to be called before the first request. Data will be overwritten each time for now.

app = FastAPI(title="Engagement Management Tool")

# Mount API routers
app.include_router(engagement_api.router)

# Setup for Jinja2 templates
templates = Jinja2Templates(directory="app/templates")
# app.mount("/static", StaticFiles(directory="app/static"), name="static") # If you add static files

# Call this manually or in an on_startup event
@app.on_event("startup")
async def on_startup():
    create_db_and_tables()

#********************************************************************************
# ******Routes for the GUI (Frontend)*******************************************
#********************************************************************************

@app.get("/", response_class=HTMLResponse, tags=["gui"])
async def list_engagements_gui(request: Request, db: Session = Depends(get_db)):
    engagements = crud.get_engagements(db)
    return templates.TemplateResponse("list_engagements.html", {"request": request, "engagements": engagements, "statuses": EngagementStatus})

@app.get("/engagements/new", response_class=HTMLResponse, tags=["gui"])
async def new_engagement_form_gui(request: Request):
    return templates.TemplateResponse("create_engagement.html", {"request": request, "statuses": EngagementStatus})

@app.post("/engagements/new", response_class=RedirectResponse, tags=["gui"])
async def create_engagement_gui(
    request: Request,
    engagement_name: str = Form(...),
    client_name: str = Form(...),
    engagement_status: EngagementStatus = Form(EngagementStatus.PROPOSED),
    start_date: Optional[str] = Form(None),
    end_date: Optional[str] = Form(None),
    scope_summary: Optional[str] = Form(None),
    project_lead: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    # Convert empty date strings to None, otherwise parse as date
    parsed_start_date = None if not start_date or start_date.strip() == "" else date.fromisoformat(start_date)
    parsed_end_date = None if not end_date or end_date.strip() == "" else date.fromisoformat(end_date)
    
    engagement_data = schemas.EngagementCreate(
        engagement_name=engagement_name,
        client_name=client_name,
        status=engagement_status,
        start_date=parsed_start_date,
        end_date=parsed_end_date,
        scope_summary=scope_summary,
        project_lead=project_lead
    )
    crud.create_engagement(db=db, engagement=engagement_data)
    return RedirectResponse(url=app.url_path_for("list_engagements_gui"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/engagements/{engagement_id}/edit", response_class=HTMLResponse, tags=["gui"])
async def edit_engagement_form_gui(engagement_id: int, request: Request, db: Session = Depends(get_db)):
    engagement = crud.get_engagement(db, engagement_id)
    if not engagement:
        raise HTTPException(status_code=404, detail="Engagement not found")
    return templates.TemplateResponse("edit_engagement.html", {"request": request, "engagement": engagement, "statuses": EngagementStatus})

@app.post("/engagements/{engagement_id}/edit", response_class=RedirectResponse, tags=["gui"])
async def update_engagement_gui(
    engagement_id: int,
    request: Request,
    engagement_name: str = Form(...),
    client_name: str = Form(...),
    engagement_status: EngagementStatus = Form(...),
    start_date: Optional[str] = Form(None),
    end_date: Optional[str] = Form(None),
    scope_summary: Optional[str] = Form(None),
    project_lead: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    # Convert empty date strings to None, otherwise parse as date
    parsed_start_date = None if not start_date or start_date.strip() == "" else date.fromisoformat(start_date)
    parsed_end_date = None if not end_date or end_date.strip() == "" else date.fromisoformat(end_date)
    
    engagement_data = schemas.EngagementUpdate(
        engagement_name=engagement_name,
        client_name=client_name,
        status=engagement_status,
        start_date=parsed_start_date,
        end_date=parsed_end_date,
        scope_summary=scope_summary,
        project_lead=project_lead
    )
    updated = crud.update_engagement(db, engagement_id=engagement_id, engagement_update=engagement_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Engagement not found for update")
    return RedirectResponse(url=app.url_path_for("list_engagements_gui"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/engagements/{engagement_id}/delete", response_class=RedirectResponse, tags=["gui"]) # Using GET for simplicity, POST is better
async def delete_engagement_gui(engagement_id: int, request: Request, db: Session = Depends(get_db)):
    crud.delete_engagement(db, engagement_id=engagement_id)
    return RedirectResponse(url=app.url_path_for("list_engagements_gui"), status_code=status.HTTP_303_SEE_OTHER)

