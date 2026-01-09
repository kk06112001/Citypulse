from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserLogin,Token,UserCreate,UserResponse
from app.core.security import verify_password, create_access_token,hash_password

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

#---- db dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#---- Login Route
@router.post("/login", response_model=Token)
def login(user_credentials:UserLogin,db:Session=Depends(get_db)):
    user=db.query(User).filter(
        User.email==user_credentials.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    if not verify_password(user_credentials.password,user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    access_token=create_access_token(
        data={
            "user_id":user.id,
            "role":user.role})
    return {"access_token":access_token,"token_type":"bearer"}
    

#---- Register Route
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session= Depends(get_db)):
    existing_user=db.query(User).filter(
        User.email==user_data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    new_user=User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        role="citizen"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user