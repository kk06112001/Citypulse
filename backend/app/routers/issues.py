from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal
from app.models.issue import Issue
from app.schemas.issue import IssueCreate, IssueResponse
from app.core.dependencies import get_current_user
from app.models.issue_history import IssueHistory
from app.schemas.issue_history import IssueHistoryResponse
router = APIRouter(
    prefix="/issues",
    tags=["Issues"]
)

# ---------- DB dependency ----------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- Create Issue (Citizen) ----------

@router.post(
    "",
    response_model=IssueResponse,
    status_code=status.HTTP_201_CREATED
)
def create_issue(
    issue_data: IssueCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    issue = Issue(
        title=issue_data.title,
        description=issue_data.description,
        category=issue_data.category,
        location=issue_data.location,
        image_url=issue_data.image_url,
        citizen_id=current_user.id,
        status="Open"
    )

    db.add(issue)
    db.commit()
    db.refresh(issue)

    return issue

# ---------- View My Issues (Citizen) ----------

@router.get(
    "/my",
    response_model=List[IssueResponse]
)
def get_my_issues(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    issues = db.query(Issue).filter(
        Issue.citizen_id == current_user.id
    ).all()

    return issues
 
# ---------- View Issue History (Citizen) ----------
@router.get(
    "/{issue_id}/history",
    response_model=list[IssueHistoryResponse]
)
def get_issue_history(
    issue_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    issue = db.query(Issue).filter(Issue.id == issue_id).first()

    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    # Citizen can see only their own issue history
    if current_user.role == "citizen" and issue.citizen_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    history = db.query(IssueHistory).filter(
        IssueHistory.issue_id == issue_id
    ).order_by(IssueHistory.changed_at).all()

    return history
