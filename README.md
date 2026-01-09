CityPulse – Real-Time Urban Issue Reporting & Resolution System

CityPulse is a civic-tech web application designed to improve how urban issues are reported, tracked, and resolved in a city. It provides a citizen-facing panel for reporting public issues and an admin/authority panel for government agencies to manage, prioritize, and resolve complaints efficiently.


Key Features
Citizen Panel

User registration and authentication

Report urban issues (potholes, garbage, streetlights, etc.)

Upload issue images

Track issue status in real time

View complaint history

Receive status updates

Admin / Authority Panel

Secure admin login

View all reported issues

Filter issues by category, area, and status

Assign issues to departments/officers

Update issue status (Open → In Progress → Resolved)

Monitor complaint resolution performance

 User Roles
Role	Description
Citizen	Reports and tracks urban issues
Admin	Reviews, assigns, and resolves complaints
 System Workflow

Citizen submits an issue

Issue is stored with status Open

Admin reviews and assigns the issue

Status changes to In Progress

Issue is resolved and marked Resolved

Citizen is notified of the update

 SDLC Coverage

Requirement Analysis: Identified needs of citizens and authorities

System Design: Role-based architecture with REST APIs

Implementation: Frontend (HTML/CSS/JS) + Backend (FastAPI)

Testing: API testing, role-based access testing

Deployment: Docker-ready backend with PostgreSQL

Maintenance: Scalable design for future enhancements

Tech Stack
Frontend

HTML

CSS

JavaScript (Vanilla JS)

Backend

Python

FastAPI

Uvicorn

Database

PostgreSQL

SQLAlchemy ORM

Other

RESTful APIs

JWT Authentication

Pydantic for data validation