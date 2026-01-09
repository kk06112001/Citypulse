from sqlalchemy import Column,Index, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class IssueHistory(Base):
    __tablename__ = "issue_history"

    id = Column(Integer, primary_key=True, index=True)
    issue_id = Column(Integer, ForeignKey("issues.id"), nullable=False)
    old_status = Column(String, nullable=True)
    new_status = Column(String, nullable=False)
    changed_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    remarks = Column(String, nullable=True)
    changed_at = Column(DateTime, default=datetime.utcnow)
    __table_args__ = (
        Index("idx_issue_history_issue_id", "issue_id"),
    )