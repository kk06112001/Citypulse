from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class IssueHistoryResponse(BaseModel):
    id: int
    issue_id: int
    old_status: Optional[str]
    new_status: str
    changed_by: int
    remarks: Optional[str]
    changed_at: datetime

    class Config:
        from_attributes = True