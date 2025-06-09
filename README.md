# Ledger - Security Assessment & Engagement Platform

## Overview (The Broader Project)

This repository contains the development of Ledger, a security assessment, engagement management, and collaboration tool. This is a semester-long class project broken into different tools to create a modular, microservices-based platform to streamline various aspects of security testing engagements.

Key intended features for the overall platform include:
* **Engagement Management:** Tracking security projects from scoping to completion.
* **Scoping & Questionnaires:** Facilitating the initial information gathering phase (e.g., using tools like Limesurvey).
* **Assessment Workflow:** Supporting penetration testing and vulnerability scanning activities.
* **Evidence Management:** Storing and organizing findings.
* **Reporting:** Assisting in the generation of security assessment reports.
* **Collaboration:** Enabling team members to work together on engagements.

The platform is being built with a focus on modularity using a microservices architecture to allow for scalability and easier integration of new features and tools over the semester.

# Enhanced Engagement Management Service/Clients - Week 3 Deliverable
## Module: Client Management (2nd Deliverable)

# Client Contact Management System

## Overview

The engagements application now includes client contact management with support for multiple contacts per client. This feature allows you to:

- Manage client information (name, company, address, phone, notes)
- Store multiple contacts per client with different email addresses
- Designate primary contacts
- Link engagements to specific clients
- View all client details and related engagements in one place

## Database Structure

### Tables Added

1. **`clients`** - Stores client information
   - `id` (Primary Key)
   - `name` (Unique, Required)
   - `company`
   - `address`
   - `phone`
   - `notes`
   - `created_at`, `updated_at`

2. **`client_contacts`** - Stores contact information for clients
   - `id` (Primary Key)
   - `client_id` (Foreign Key to clients.id)
   - `name` (Required)
   - `email` (Required, validated)
   - `title`
   - `phone`
   - `is_primary` ("yes" or "no")
   - `created_at`, `updated_at`

3. **`engagements`** - Updated to reference clients
   - Added `client_id` (Foreign Key to clients.id)
   - Kept `client_name` for backward compatibility

## API Endpoints

### Client Management

- `GET /api/v1/clients` - List all clients
- `POST /api/v1/clients` - Create new client (with contacts)
- `GET /api/v1/clients/{client_id}` - Get client details
- `PUT /api/v1/clients/{client_id}` - Update client
- `DELETE /api/v1/clients/{client_id}` - Delete client

### Contact Management

- `POST /api/v1/clients/{client_id}/contacts` - Add contact to client
- `GET /api/v1/clients/{client_id}/contacts` - List client contacts
- `GET /api/v1/clients/{client_id}/contacts/{contact_id}` - Get contact details
- `PUT /api/v1/clients/{client_id}/contacts/{contact_id}` - Update contact
- `DELETE /api/v1/clients/{client_id}/contacts/{contact_id}` - Delete contact

## Web Interface

### Navigation
- Added "Clients List" and "New Client" links to main navigation
- Available at: `http://localhost:8000/clients`

### Client Management Pages

1. **Client List** (`/clients`)
   - Shows all clients with primary contact information
   - Actions: View, Edit, Delete

2. **Create Client** (`/clients/new`)
   - Create client with multiple contacts
   - JavaScript-powered interface to add/remove contacts
   - Automatic primary contact designation

3. **View Client** (`/clients/{client_id}`)
   - Complete client information
   - All contacts with management actions
   - Related engagements
   - Quick actions to add contacts

4. **Edit Client** (`/clients/{client_id}/edit`)
   - Update client information
   - Separate contact management

### Contact Management

1. **Add Contact** (`/clients/{client_id}/contacts/new`)
2. **Edit Contact** (`/clients/{client_id}/contacts/{contact_id}/edit`)
3. **Delete Contact** - Confirmation dialog

### Updated Engagement Management

- **Create Engagement**: Now uses client dropdown instead of text input
- **Edit Engagement**: Client selection from existing clients
- Automatic client name population from selected client

## Usage Examples

### Creating a Client with Multiple Contacts

```json
POST /api/v1/clients
{
  "name": "Acme Corporation",
  "company": "Acme Corp",
  "address": "123 Business St, City, State 12345",
  "phone": "+1-555-0123",
  "notes": "Important client",
  "contacts": [
    {
      "name": "John Smith",
      "email": "john.smith@acme.com",
      "title": "IT Director",
      "phone": "+1-555-0124",
      "is_primary": "yes"
    },
    {
      "name": "Jane Doe",
      "email": "jane.doe@acme.com",
      "title": "Security Manager",
      "phone": "+1-555-0125",
      "is_primary": "no"
    }
  ]
}
```

### Adding Additional Contact

```json
POST /api/v1/clients/1/contacts
{
  "name": "Bob Johnson",
  "email": "bob.johnson@acme.com",
  "title": "CTO",
  "phone": "+1-555-0126",
  "is_primary": "no"
}
```

## Features

### Email Validation
- Uses Pydantic EmailStr for automatic email validation
- Ensures all email addresses are properly formatted

### Primary Contact Management
- Each client can have one primary contact
- Primary contact is highlighted in listings
- Automatic fallback to first contact if no primary designated

### Relationship Management
- Clients can have multiple engagements
- Engagements are linked to clients via foreign key
- View all client engagements from client detail page

### Data Integrity
- Foreign key constraints ensure data consistency
- Cascade delete: Deleting a client removes all contacts and updates engagements
- Unique client names prevent duplicates

## Database Relationships

```
clients (1) -----> (*) client_contacts
   |
   | (1)
   |
   v
   (*) engagements
```

## Migration Notes

- New installations will create all tables automatically
- Existing engagements will need client_id populated
- Backward compatibility maintained with client_name field
- No data loss during updates

## Security Considerations

- Email validation prevents malformed addresses
- Client names must be unique
- Proper foreign key constraints
- Input sanitization on all forms

## Testing

Access the application at `http://localhost:8000` to test:

1. Create a new client with multiple contacts
2. View client details and contact information
3. Create an engagement linked to the client
4. Edit client and contact information
5. Test email validation and primary contact features


## Module: Engagement Management Service (1st Deliverable)

### Description

The Engagement Management Service is a microservice responsible for creating, tracking, and managing security assessment engagements. It provides a persistent store for engagement details and exposes a RESTful API for programmatic access, along with a basic web interface for testing and demonstration.

### Features (1st Deliverable)

* **CRUD Operations:** Create, Read, Update, and Delete (CRUD) security engagements.
* **Data Fields:** Manages engagement details such as name, client, status (Proposed, Scoping, Scheduled, In Progress, On Hold, Completed, Cancelled), start/end dates, scope summary, and project lead.
* **REST API:** An API for interacting with engagement data.
    * Automatic API documentation available via Swagger UI (`/docs`) and ReDoc (`/redoc`).
* **Simple Web GUI:** A basic HTML interface for listing, creating, editing, and deleting engagements, primarily for testing and ease of use during early development.
* **Data Persistence:** Engagement data is stored in a PostgreSQL database.
* **Containerized Application:** The service and its database run in Docker containers, managed by Docker Compose for easy setup and deployment.

### Technology Stack

* **Backend Framework:** Python 3.11+ with FastAPI
* **Database:** PostgreSQL 15
* **Data Validation & Serialization:** Pydantic v1.10.22
* **ORM (Object-Relational Mapper):** SQLAlchemy
* **API Documentation:** OpenAPI (auto-generated by FastAPI)
* **Containerization:** Docker & Docker Compose
* **Web Interface (GUI Placeholder):** Jinja2 templates with basic HTML/CSS

### Project Structure

The core application code for this service resides within the `app/` directory:

```
Tools/engagements/
├── app/
│   ├── main.py                    # FastAPI application instance, GUI routes, startup events
│   ├── models.py                  # SQLAlchemy database models
│   ├── schemas.py                 # Pydantic data schemas for API requests/responses
│   ├── crud.py                    # Core CRUD logic for database interactions
│   ├── database.py                # Database connection setup and session management
│   ├── routers/
│   │   └── engagement_api.py      # API endpoint definitions
│   └── templates/                 # HTML templates for the simple web GUI
│       ├── base.html
│       ├── create_engagement.html
│       ├── edit_engagement.html
│       └── list_engagements.html
├── Dockerfile                     # Defines the Docker image for the FastAPI application
├── docker-compose.yml             # Orchestrates the application and database services
├── requirements.txt               # Lists Python dependencies
└── .gitignore                     # Git ignore file
```

### Prerequisites

* Docker Desktop (or Docker Engine + Docker Compose CLI) installed and running.
* Git (for cloning the repository).

### Setup & Running

1.  **Navigate to Project Directory:**
    ```bash
    cd Tools/engagements
    ```

2.  **Build and Run with Docker Compose:**
    Open a terminal in the project directory and run:
    ```bash
    docker-compose up --build
    ```
    This command will build the Docker image for the application (if it doesn't exist or if `Dockerfile` changed) and start both the FastAPI application service and the PostgreSQL database service.
    * Use `docker-compose up` to start if images are already built.
    * Add `-d` to run in detached mode: `docker-compose up --build -d`

3.  **Accessing the Service:**
    * **Simple Web GUI:** Open your web browser and go to `http://localhost:8000/`
    * **API Documentation (Swagger UI):** `http://localhost:8000/docs`
    * **Alternative API Documentation (ReDoc):** `http://localhost:8000/redoc`

### API Endpoints

The REST API provides the following endpoints:

* **GET** `/api/v1/engagements` - List all engagements (with optional skip/limit pagination)
* **POST** `/api/v1/engagements` - Create a new engagement
* **GET** `/api/v1/engagements/{engagement_id}` - Get a specific engagement by ID
* **PUT** `/api/v1/engagements/{engagement_id}` - Update an existing engagement
* **DELETE** `/api/v1/engagements/{engagement_id}` - Delete an engagement

### Data Model

Each engagement contains the following fields:

* **id** (integer): Auto-generated unique identifier
* **engagement_name** (string): Name of the engagement -- Might auto generate this in the future.
* **client_name** (string): Name of the client
* **status** (enum): Current status of the engagement
  * Proposed
  * Scoping
  * Scheduled
  * In Progress
  * On Hold
  * Completed
  * Cancelled
* **start_date** (date, optional): Planned or actual start date
* **end_date** (date, optional): Planned or actual end date
* **scope_summary** (text, optional): Brief description of the engagement scope
* **project_lead** (string, optional): Name of the project lead
* **created_at** (datetime): Timestamp when the engagement was created
* **updated_at** (datetime): Timestamp when the engagement was last updated

### How to Use

#### Via the Web GUI:
* Navigate to `http://localhost:8000/` to see a list of current engagements.
* Click "Create New Engagement" to add a new one using the form.
* From the list, you can "Edit" or "Delete" existing engagements.

#### Via the API:
* Use the interactive API documentation at `http://localhost:8000/docs` to test endpoints.
* You can also use tools like Postman or `curl` to send requests to the API endpoints.

**Example API Usage:**
```bash
# List all engagements
curl -X GET "http://localhost:8000/api/v1/engagements"

# Create a new engagement
curl -X POST "http://localhost:8000/api/v1/engagements" \
     -H "Content-Type: application/json" \
     -d '{
       "engagement_name": "Security Assessment",
       "client_name": "Acme Corp",
       "status": "Proposed",
       "start_date": "2024-01-15",
       "project_lead": "John Doe"
     }'

# Get a specific engagement
curl -X GET "http://localhost:8000/api/v1/engagements/1"
```

### Database Configuration

The application uses PostgreSQL with the following default configuration (defined in `docker-compose.yml`):
* **Host:** db (Docker service name)
* **Port:** 5432
* **Database:** engagementdb
* **Username:** user
* **Password:** password

**Note:** For production use, these credentials should be changed and stored in environment variables.

### Development Notes

* The application uses Pydantic v1.10.22 syntax (not v2--hopefully changing this)
* Database tables are automatically created on application startup
* The application includes live reloading for development (changes to code are reflected immediately)

### Stopping the Application

To stop the running containers:
```bash
docker-compose down
```

To stop and remove all data (including the database):
```bash
docker-compose down -v
```

---

**Next Steps:** Future deliverables will include enhanced security features, user authentication, advanced reporting capabilities, and integration with other security tools. 
