from sqlalchemy import Column, Index, Integer, Boolean, String, ForeignKey, DateTime
from datetime import datetime
from app.database import Base

class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    message = Column(String, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    __table_args__ = (
        Index("idx_notifications_user_id", "user_id"),
    )
