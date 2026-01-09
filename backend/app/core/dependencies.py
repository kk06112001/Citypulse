from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.core.config import SECRET_KEY, ALGORITHM
from app.database import SessionLocal
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

#----Database Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#----Get Current User Dependency
def get_current_user(
        token: str=Depends(oauth2_scheme),
        db:Session=Depends(get_db)
):
    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"},
    )
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id:int=payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    
    user=db.query(User).filter(User.id==user_id).first()
    if user is None:
        raise credentials_exception
    
    return user
def require_role(required_role: str):
    def role_checker(current_user=Depends(get_current_user)):
        if current_user.role!=required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted"
            )
        return current_user
    return role_checker

def get_current_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user