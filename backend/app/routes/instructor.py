from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from ..database import get_db
from ..models import PRReview, ReviewStatus
from ..schemas import InstructorDecision, PRReviewResponse
from ..services.github_service import GitHubService
from ..config import get_settings

router = APIRouter()
settings = get_settings()

@router.post("/reviews/{review_id}/decide", response_model=PRReviewResponse)
def instructor_decision(
    review_id: int,
    decision: InstructorDecision,
    db: Session = Depends(get_db)
):
    """Instructor approves or rejects a review"""
    
    review = db.query(PRReview).filter(PRReview.id == review_id).first()
    
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    if review.status != ReviewStatus.PENDING:
        raise HTTPException(
            status_code=400, 
            detail=f"Review is not pending (current status: {review.status})"
        )
    
    if decision.decision == "approve":
        # Post the review to GitHub
        github_service = GitHubService(settings.github_token)
        
        comment_body = review.review_summary
        
        if decision.notes:
            comment_body += f"\n\n---\n**Instructor Notes:**\n{decision.notes}"
        
        success = github_service.post_review_comment(
            review.repo_full_name,
            review.pr_number,
            comment_body,
            review.commit_sha
        )
        
        if success:
            review.status = ReviewStatus.POSTED
            review.posted_at = datetime.utcnow()
        else:
            raise HTTPException(status_code=500, detail="Failed to post to GitHub")
    
    elif decision.decision == "reject":
        review.status = ReviewStatus.REJECTED
    
    else:
        raise HTTPException(status_code=400, detail="Invalid decision")
    
    review.instructor_notes = decision.notes
    review.reviewed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(review)
    
    return review

@router.get("/reviews/stats/summary")
def get_stats(db: Session = Depends(get_db)):
    """Get review statistics"""
    
    total = db.query(PRReview).count()
    pending = db.query(PRReview).filter(PRReview.status == ReviewStatus.PENDING).count()
    approved = db.query(PRReview).filter(PRReview.status == ReviewStatus.POSTED).count()
    rejected = db.query(PRReview).filter(PRReview.status == ReviewStatus.REJECTED).count()
    
    return {
        "total": total,
        "pending": pending,
        "approved": approved,
        "rejected": rejected
    }