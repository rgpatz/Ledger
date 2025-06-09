from fastapi import FastAPI, Depends, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles # If you add CSS/JS
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import create_db_and_tables, get_db
from app.routers import engagement_api, client_api
from app import crud, schemas, models # app refers to the 'app' directory
from app.models import EngagementStatus # Import the enum
from datetime import date
from typing import Optional

# Create database tables on startup, Alembic will be used later, need to figure out how to do this in a production environment. Needs to be called before the first request. Data will be overwritten each time for now.

app = FastAPI(title="Engagement Management Tool")

# Mount API routers
app.include_router(engagement_api.router)
app.include_router(client_api.router)

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
async def new_engagement_form_gui(request: Request, db: Session = Depends(get_db)):
    clients = crud.get_clients(db)
    return templates.TemplateResponse("create_engagement.html", {"request": request, "statuses": EngagementStatus, "clients": clients})

@app.post("/engagements/new", response_class=RedirectResponse, tags=["gui"])
async def create_engagement_gui(
    request: Request,
    engagement_name: str = Form(...),
    client_id: int = Form(...),
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
    
    # Get client name from client_id
    client = crud.get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    engagement_data = schemas.EngagementCreate(
        engagement_name=engagement_name,
        client_id=client_id,
        client_name=client.name,  # Keep for backward compatibility
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
    clients = crud.get_clients(db)
    return templates.TemplateResponse("edit_engagement.html", {"request": request, "engagement": engagement, "statuses": EngagementStatus, "clients": clients})

@app.post("/engagements/{engagement_id}/edit", response_class=RedirectResponse, tags=["gui"])
async def update_engagement_gui(
    engagement_id: int,
    request: Request,
    engagement_name: str = Form(...),
    client_id: int = Form(...),
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
    
    # Get client name from client_id
    client = crud.get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    engagement_data = schemas.EngagementUpdate(
        engagement_name=engagement_name,
        client_id=client_id,
        client_name=client.name,  # Keep for backward compatibility
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

#********************************************************************************
# ******Client Management GUI Routes********************************************
#********************************************************************************

@app.get("/clients", response_class=HTMLResponse, tags=["gui"])
async def list_clients_gui(request: Request, db: Session = Depends(get_db)):
    clients = crud.get_clients(db)
    return templates.TemplateResponse("list_clients.html", {"request": request, "clients": clients})

@app.get("/clients/new", response_class=HTMLResponse, tags=["gui"])
async def new_client_form_gui(request: Request):
    return templates.TemplateResponse("create_client.html", {"request": request})

@app.post("/clients/new", response_class=RedirectResponse, tags=["gui"])
async def create_client_gui(
    request: Request,
    name: str = Form(...),
    company: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    # Process form data - extract all contact_* fields
    form_data = await request.form()
    contacts = []
    
    # Extract contact data
    contact_index = 0
    while f"contact_{contact_index}_name" in form_data:
        contact_name = form_data.get(f"contact_{contact_index}_name")
        contact_email = form_data.get(f"contact_{contact_index}_email")
        contact_title = form_data.get(f"contact_{contact_index}_title", "")
        contact_phone = form_data.get(f"contact_{contact_index}_phone", "")
        is_primary = "yes" if f"contact_{contact_index}_is_primary" in form_data else "no"
        
        if contact_name and contact_email:
            contact_data = schemas.ClientContactCreate(
                name=contact_name,
                email=contact_email,
                title=contact_title if contact_title else None,
                phone=contact_phone if contact_phone else None,
                is_primary=is_primary
            )
            contacts.append(contact_data)
        
        contact_index += 1
    
    # Ensure at least one contact is marked as primary
    if contacts and not any(c.is_primary == "yes" for c in contacts):
        contacts[0].is_primary = "yes"
    
    client_data = schemas.ClientCreate(
        name=name,
        company=company if company else None,
        address=address if address else None,
        phone=phone if phone else None,
        notes=notes if notes else None,
        contacts=contacts
    )
    
    try:
        crud.create_client(db=db, client=client_data)
        return RedirectResponse(url=app.url_path_for("list_clients_gui"), status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        # Handle duplicate client name or other errors
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/clients/{client_id}", response_class=HTMLResponse, tags=["gui"])
async def view_client_gui(client_id: int, request: Request, db: Session = Depends(get_db)):
    client = crud.get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return templates.TemplateResponse("view_client.html", {"request": request, "client": client})

@app.get("/clients/{client_id}/edit", response_class=HTMLResponse, tags=["gui"])
async def edit_client_form_gui(client_id: int, request: Request, db: Session = Depends(get_db)):
    client = crud.get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return templates.TemplateResponse("edit_client.html", {"request": request, "client": client})

@app.post("/clients/{client_id}/edit", response_class=RedirectResponse, tags=["gui"])
async def update_client_gui(
    client_id: int,
    request: Request,
    name: str = Form(...),
    company: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    client_data = schemas.ClientUpdate(
        name=name,
        company=company if company else None,
        address=address if address else None,
        phone=phone if phone else None,
        notes=notes if notes else None
    )
    updated = crud.update_client(db, client_id=client_id, client_update=client_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Client not found for update")
    return RedirectResponse(url=app.url_path_for("view_client_gui", client_id=client_id), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/clients/{client_id}/delete", response_class=RedirectResponse, tags=["gui"])
async def delete_client_gui(client_id: int, request: Request, db: Session = Depends(get_db)):
    crud.delete_client(db, client_id=client_id)
    return RedirectResponse(url=app.url_path_for("list_clients_gui"), status_code=status.HTTP_303_SEE_OTHER)

# Contact management routes

@app.get("/clients/{client_id}/contacts/new", response_class=HTMLResponse, tags=["gui"])
async def add_contact_form_gui(client_id: int, request: Request, db: Session = Depends(get_db)):
    client = crud.get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return templates.TemplateResponse("add_contact.html", {"request": request, "client": client})

@app.post("/clients/{client_id}/contacts/new", response_class=RedirectResponse, tags=["gui"])
async def create_contact_gui(
    client_id: int,
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    title: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    is_primary: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    contact_data = schemas.ClientContactCreate(
        name=name,
        email=email,
        title=title if title else None,
        phone=phone if phone else None,
        is_primary="yes" if is_primary else "no"
    )
    crud.create_contact(db=db, contact=contact_data, client_id=client_id)
    return RedirectResponse(url=app.url_path_for("view_client_gui", client_id=client_id), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/clients/{client_id}/contacts/{contact_id}/edit", response_class=HTMLResponse, tags=["gui"])
async def edit_contact_form_gui(client_id: int, contact_id: int, request: Request, db: Session = Depends(get_db)):
    contact = crud.get_contact(db, contact_id)
    if not contact or contact.client_id != client_id:
        raise HTTPException(status_code=404, detail="Contact not found")
    client = crud.get_client(db, client_id)
    return templates.TemplateResponse("edit_contact.html", {"request": request, "client": client, "contact": contact})

@app.post("/clients/{client_id}/contacts/{contact_id}/edit", response_class=RedirectResponse, tags=["gui"])
async def update_contact_gui(
    client_id: int,
    contact_id: int,
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    title: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    is_primary: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    contact_data = schemas.ClientContactUpdate(
        name=name,
        email=email,
        title=title if title else None,
        phone=phone if phone else None,
        is_primary="yes" if is_primary else "no"
    )
    updated = crud.update_contact(db, contact_id=contact_id, contact_update=contact_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Contact not found for update")
    return RedirectResponse(url=app.url_path_for("view_client_gui", client_id=client_id), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/clients/{client_id}/contacts/{contact_id}/delete", response_class=RedirectResponse, tags=["gui"])
async def delete_contact_gui(client_id: int, contact_id: int, request: Request, db: Session = Depends(get_db)):
    crud.delete_contact(db, contact_id=contact_id)
    return RedirectResponse(url=app.url_path_for("view_client_gui", client_id=client_id), status_code=status.HTTP_303_SEE_OTHER)

