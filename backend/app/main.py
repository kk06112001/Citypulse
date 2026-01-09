from fastapi import FastAPI
from app.database import Base, SessionLocal,engine
from app.models.user import User
from app.core.security import hash_password
from app.routers import auth,admin,users,issues,notifications
from app.models import issue,issue_history,notification
from fastapi.middleware.cors import CORSMiddleware
app=FastAPI(title="CityPulse API",version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only, allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # <-- this allows OPTIONS preflight
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(issues.router)
app.include_router(notifications.router)
Base.metadata.create_all(bind=engine)

def create_admin():
    db=SessionLocal()
    admin_email="admin@citypulse.com"
    admin_password="admin123"

    admin=db.query(User).filter(User.email==admin_email).first()
    if not admin:
        new_admin=User(
            name="System Admin",
            email=admin_email,
            password_hash=hash_password(admin_password),
            role="admin"
        )
        db.add(new_admin)
        db.commit()
        print("Admin user created with email:",admin_email,"and password:",admin_password)
    db.close()

create_admin()
@app.get("/")
def root():
    return {"message":"Welcome to the CityPulse API"}