from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.notification import Notification
from app.schemas.notification import NotificationResponse
from app.core.dependencies import get_current_user
from app.database import SessionLocal
router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
#----Get Notifications for Current User
@router.get("/", response_model=list[NotificationResponse])
def get_notifications(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(Notification).filter(
        Notification.user_id==current_user.id
    ).order_by(Notification.created_at.desc()).all()

#----Mark Notification as Read
@router.patch("/{notification_id}/read")
def mark_notification_read(
    notification_id: int,
    db: Session=Depends(get_db),
    current_user=Depends(get_current_user)
):
    notification=db.query(Notification).filter(
        Notification.id==notification_id,
        Notification.user_id==current_user.id
    ).first()

    if notification:
        notification.is_read=True
        db.commit()
        return {"message":"Notification marked as read"}
