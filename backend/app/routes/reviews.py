from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import PRReview, ReviewStatus
from ..schemas import PRReviewResponse

router = APIRouter()

@router.get("/reviews", response_model=List[PRReviewResponse])
def get_all_reviews(
    status: str = None,
    db: Session = Depends(get_db)
):
    """Get all reviews, optionally filtered by status"""
    query = db.query(PRReview)
    
    if status:
        try:
            status_enum = ReviewStatus(status)
            query = query.filter(PRReview.status == status_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid status")
    
    reviews = query.order_by(PRReview.created_at.desc()).all()
    return reviews

@router.get("/reviews/{review_id}", response_model=PRReviewResponse)
def get_review(review_id: int, db: Session = Depends(get_db)):
    """Get a specific review"""
    review = db.query(PRReview).filter(PRReview.id == review_id).first()
    
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    return review