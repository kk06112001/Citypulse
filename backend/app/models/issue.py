from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from datetime import datetime
from app.database import Base

class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    category = Column(String, nullable=False, index=True)
    location = Column(String, nullable=False, index=True)

    status = Column(String, default="Open", index=True)  # Open | In Progress | Resolved

    image_url = Column(String, nullable=True)

    citizen_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    assigned_to = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    __table_args__ = (
        Index("idx_issues_status", "status"),
        Index("idx_issues_category", "category"),
        Index("idx_issues_location", "location"),
        Index("idx_issues_citizen_id", "citizen_id"),
    )
