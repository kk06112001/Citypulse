from fastapi import APIRouter, Depends, HTTPException, status,Query
from app.core.dependencies import require_role
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import SessionLocal
from app.models.issue import Issue
from app.models.user import User
from app.core.dependencies import get_current_admin
from app.models.issue_history import IssueHistory
from app.schemas.issue import AdminIssueResponse,IssueAssign,IssueStatusUpdate
from app.models.notification import Notification
ALLOWED_STATUS_TRANSITIONS = {
    "Open": ["In Progress"],
    "In Progress": ["Resolved"],
    "Resolved": []
}

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#--admin dashboard 
@router.get("/dashboard")
def admin_dashboard(
    current_admin=Depends(require_role("admin"))
):
    return{
        "message":"Welcome, Admin",
        "admin_id": current_admin.id,
        "email": current_admin.email
    }

#--view all issues with filters
@router.get("/issues", response_model=List[AdminIssueResponse])
def get_all_issues(db: Session = Depends(get_db), current_admin: User = Depends(require_role("admin"))):
    issues = db.query(Issue).all()
    
    # Add citizen email
    result = []
    for issue in issues:
        citizen = db.query(User).filter(User.id == issue.citizen_id).first()
        issue_dict = issue.__dict__.copy()
        issue_dict['citizen_email'] = citizen.email if citizen else None
        result.append(issue_dict)
    
    return result


#--assign issue to staff
@router.put("/issues/{issue_id}/assign")
def assign_issue(issue_id: int, assign_data: IssueAssign, 
                 db: Session = Depends(get_db),
                 current_admin: User = Depends(get_current_admin)):
    
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    old_status = issue.status
    issue.assigned_to = assign_data.assigned_to
    issue.status = "In Progress"

    # Add history
    history = IssueHistory(
        issue_id=issue.id,
        old_status=old_status,
        new_status="In Progress",
        changed_by=current_admin.id,
        remarks=f"Assigned to {assign_data.assigned_to}"
    )
    db.add(history)
    db.commit()
    return {"detail": "Issue assigned successfully"}

#--update issue status
@router.patch("/issues/{issue_id}/status")  # PATCH is fine
def update_issue_status(
    issue_id: int,
    status_data: IssueStatusUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_role("admin"))
):
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue not found"
        )

    current_status = issue.status
    new_status = status_data.status

    # Enforce allowed transitions
    if new_status not in ALLOWED_STATUS_TRANSITIONS[current_status]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status transition: {current_status} → {new_status}"
        )

    # Update issue
    old_status = issue.status
    issue.status = new_status

    # Add history
    history = IssueHistory(
        issue_id=issue.id,
        old_status=old_status,
        new_status=new_status,
        changed_by=current_admin.id,
        remarks="Status updated"
    )
    db.add(history)

    # Add notification
    notification = Notification(
        user_id=issue.citizen_id,
        message=f"Your issue #{issue.id} status changed to {new_status}"
    )
    db.add(notification)

    db.commit()

    return {"message": f"Issue status updated to {new_status}"}