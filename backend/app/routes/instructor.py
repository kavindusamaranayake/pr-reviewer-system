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



# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from datetime import datetime

# from ..database import get_db
# from ..models import PRReview, ReviewStatus
# from ..schemas import InstructorDecision, PRReviewResponse
# from ..services.github_service import GitHubService
# from ..config import get_settings

# router = APIRouter()
# settings = get_settings()

# @router.post("/reviews/{review_id}/decide", response_model=PRReviewResponse)
# def instructor_decision(
#     review_id: int,
#     decision: InstructorDecision,
#     db: Session = Depends(get_db)
# ):
#     """Instructor approves or rejects a review"""
    
#     review = db.query(PRReview).filter(PRReview.id == review_id).first()
    
#     if not review:
#         raise HTTPException(status_code=404, detail="Review not found")
    
#     if review.status != ReviewStatus.PENDING:
#         raise HTTPException(
#             status_code=400, 
#             detail=f"Review is not pending (current status: {review.status})"
#         )
    
#     github_service = GitHubService(settings.github_token)
    
#     if decision.decision == "approve":
#         # Post the review to GitHub
#         comment_body = review.review_summary
        
#         if decision.notes:
#             comment_body += f"\n\n---\n**Instructor Notes:**\n{decision.notes}"
        
#         # Add merge status to comment
#         if decision.auto_merge:
#             comment_body += f"\n\n---\n🤖 **Auto-merge enabled** - This PR will be merged automatically if all checks pass."
        
#         success = github_service.post_review_comment(
#             review.repo_full_name,
#             review.pr_number,
#             comment_body,
#             review.commit_sha
#         )
        
#         if not success:
#             raise HTTPException(status_code=500, detail="Failed to post to GitHub")
        
#         review.status = ReviewStatus.POSTED
#         review.posted_at = datetime.utcnow()
        
#         # Auto-merge if requested
#         merge_result = {"success": False, "message": "Auto-merge not requested"}
        
#         if decision.auto_merge:
#             # Check PR status first
#             pr_status = github_service.check_pr_status(
#                 review.repo_full_name,
#                 review.pr_number
#             )
            
#             if pr_status.get("can_merge", False):
#                 # Merge the PR
#                 merge_message = f"Auto-merged by instructor after review approval\n\n{decision.notes or ''}"
#                 merge_result = github_service.merge_pull_request(
#                     review.repo_full_name,
#                     review.pr_number,
#                     commit_message=merge_message,
#                     merge_method="merge"  # or "squash" or "rebase"
#                 )
                
#                 if merge_result["success"]:
#                     # Post success comment
#                     github_service.post_review_comment(
#                         review.repo_full_name,
#                         review.pr_number,
#                         "✅ **PR has been automatically merged by instructor**",
#                         review.commit_sha
#                     )
#             else:
#                 # Cannot merge - post explanation
#                 reason = "unknown reason"
#                 if not pr_status.get("mergeable"):
#                     reason = "merge conflicts"
#                 elif pr_status.get("status_checks", {}).get("state") != "success":
#                     reason = "status checks not passing"
                
#                 github_service.post_review_comment(
#                     review.repo_full_name,
#                     review.pr_number,
#                     f"⚠️ **Auto-merge failed**: PR cannot be merged due to {reason}. Please resolve and merge manually.",
#                     review.commit_sha
#                 )
#                 merge_result = {
#                     "success": False,
#                     "message": f"Cannot merge: {reason}"
#                 }
    
#     elif decision.decision == "reject":
#         review.status = ReviewStatus.REJECTED
#         merge_result = {"success": False, "message": "Review rejected"}
    
#     else:
#         raise HTTPException(status_code=400, detail="Invalid decision")
    
#     review.instructor_notes = decision.notes
#     review.reviewed_at = datetime.utcnow()
    
#     # Store merge result if auto-merge was attempted
#     if decision.auto_merge and decision.decision == "approve":
#         if not review.instructor_notes:
#             review.instructor_notes = ""
#         review.instructor_notes += f"\n\nAuto-merge result: {merge_result['message']}"
    
#     db.commit()
#     db.refresh(review)
    
#     return review

# @router.get("/reviews/stats/summary")
# def get_stats(db: Session = Depends(get_db)):
#     """Get review statistics"""
    
#     total = db.query(PRReview).count()
#     pending = db.query(PRReview).filter(PRReview.status == ReviewStatus.PENDING).count()
#     approved = db.query(PRReview).filter(PRReview.status == ReviewStatus.POSTED).count()
#     rejected = db.query(PRReview).filter(PRReview.status == ReviewStatus.REJECTED).count()
    
#     return {
#         "total": total,
#         "pending": pending,
#         "approved": approved,
#         "rejected": rejected
#     }

# @router.get("/reviews/{review_id}/pr-status")
# def get_pr_merge_status(
#     review_id: int,
#     db: Session = Depends(get_db)
# ):
#     """Check if PR can be merged"""
    
#     review = db.query(PRReview).filter(PRReview.id == review_id).first()
    
#     if not review:
#         raise HTTPException(status_code=404, detail="Review not found")
    
#     github_service = GitHubService(settings.github_token)
#     pr_status = github_service.check_pr_status(
#         review.repo_full_name,
#         review.pr_number
#     )
    
#     return pr_status




