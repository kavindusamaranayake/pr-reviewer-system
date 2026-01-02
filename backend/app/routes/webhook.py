from fastapi import APIRouter, Request, Depends, HTTPException, Header
from sqlalchemy.orm import Session
import hmac
import hashlib
from typing import Optional

from ..database import get_db
from ..config import get_settings
from ..models import PRReview, ReviewStatus
from ..services.review_engine import ReviewEngine
from ..services.branch_rules import BranchRulesService

router = APIRouter()
settings = get_settings()

def verify_signature(payload: bytes, signature: str) -> bool:
    """Verify GitHub webhook signature"""
    if not signature:
        return False
    
    sha_name, github_signature = signature.split('=')
    if sha_name != 'sha256':
        return False
    
    mac = hmac.new(
        settings.github_webhook_secret.encode(),
        msg=payload,
        digestmod=hashlib.sha256
    )
    
    return hmac.compare_digest(mac.hexdigest(), github_signature)

@router.post("/webhook/github")
async def github_webhook(
    request: Request,
    db: Session = Depends(get_db),
    x_hub_signature_256: Optional[str] = Header(None)
):
    """Receive GitHub webhook events"""
    
    # Get raw body for signature verification
    body = await request.body()
    
    # Verify signature
    if not verify_signature(body, x_hub_signature_256 or ""):
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    # Parse JSON
    payload = await request.json()
    
    # Only process pull_request events
    if "pull_request" not in payload:
        return {"message": "Event ignored"}
    
    action = payload.get("action")
    
    # Only process opened and synchronize (new commits) events
    if action not in ["opened", "synchronize"]:
        return {"message": "Action ignored"}
    
    pr_data = payload["pull_request"]
    repo_data = payload["repository"]
    
    # Extract PR information
    pr_number = pr_data["number"]
    repo_full_name = repo_data["full_name"]
    branch_name = pr_data["head"]["ref"]
    pr_title = pr_data["title"]
    pr_author = pr_data["user"]["login"]
    pr_url = pr_data["html_url"]
    commit_sha = pr_data["head"]["sha"]
    
    # Get branch-based expectations
    branch_service = BranchRulesService(db)
    expectations = branch_service.get_expectations_for_branch(branch_name)
    branch_type = branch_service.extract_branch_type(branch_name)
    
    # Run automated review
    review_engine = ReviewEngine(settings.github_token)
    review_result = review_engine.analyze_pr(
        repo_full_name,
        pr_number,
        expectations
    )
    
    # Check if review already exists
    existing_review = db.query(PRReview).filter(
        PRReview.pr_number == pr_number,
        PRReview.repo_full_name == repo_full_name,
        PRReview.commit_sha == commit_sha
    ).first()
    
    if existing_review:
        # Update existing review
        existing_review.review_feedback = review_result["feedback_items"]
        existing_review.review_summary = review_result["summary"]
        existing_review.expectations_applied = expectations
        existing_review.status = ReviewStatus.PENDING
    else:
        # Create new review
        pr_review = PRReview(
            pr_number=pr_number,
            repo_full_name=repo_full_name,
            branch_name=branch_name,
            branch_type=branch_type,
            pr_title=pr_title,
            pr_author=pr_author,
            review_feedback=review_result["feedback_items"],
            review_summary=review_result["summary"],
            expectations_applied=expectations,
            status=ReviewStatus.PENDING,
            pr_url=pr_url,
            commit_sha=commit_sha
        )
        db.add(pr_review)
    
    db.commit()
    
    return {
        "message": "PR review created and pending instructor approval",
        "pr_number": pr_number,
        "branch_type": branch_type
    }