from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
from .models import ReviewStatus

class ReviewFeedbackItem(BaseModel):
    category: str
    severity: str  # info, warning, error
    message: str
    line_number: Optional[int] = None
    file_path: Optional[str] = None

class PRReviewCreate(BaseModel):
    pr_number: int
    repo_full_name: str
    branch_name: str
    pr_title: str
    pr_author: str
    pr_url: str
    commit_sha: str

class PRReviewResponse(BaseModel):
    id: int
    pr_number: int
    repo_full_name: str
    branch_name: str
    branch_type: str
    pr_title: str
    pr_author: str
    review_feedback: List[Dict[str, Any]]
    review_summary: str
    expectations_applied: Dict[str, Any]
    status: ReviewStatus
    instructor_notes: Optional[str]
    created_at: datetime
    pr_url: str
    
    class Config:
        from_attributes = True

class InstructorDecision(BaseModel):
    decision: str  # "approve" or "reject"
    notes: Optional[str] = None
    

class BranchRuleCreate(BaseModel):
    branch_pattern: str
    description: str
    expectations: Dict[str, Any]

class BranchRuleResponse(BaseModel):
    id: int
    branch_pattern: str
    description: str
    expectations: Dict[str, Any]
    created_at: datetime
    
    class Config:
        from_attributes = True