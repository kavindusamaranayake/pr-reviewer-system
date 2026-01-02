from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, JSON
from sqlalchemy.sql import func
import enum
from .database import Base

class ReviewStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    POSTED = "posted"

class PRReview(Base):
    __tablename__ = "pr_reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    pr_number = Column(Integer, nullable=False)
    repo_full_name = Column(String, nullable=False)
    branch_name = Column(String, nullable=False)
    branch_type = Column(String, nullable=False)  # feature, bugfix, hotfix, etc.
    pr_title = Column(String, nullable=False)
    pr_author = Column(String, nullable=False)
    
    # Review content
    review_feedback = Column(JSON, nullable=False)  # Structured feedback
    review_summary = Column(Text, nullable=False)
    expectations_applied = Column(JSON, nullable=False)  # Branch-based rules
    
    # Status tracking
    status = Column(Enum(ReviewStatus), default=ReviewStatus.PENDING)
    instructor_notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    posted_at = Column(DateTime(timezone=True), nullable=True)
    
    # GitHub data
    pr_url = Column(String, nullable=False)
    commit_sha = Column(String, nullable=False)

class BranchRule(Base):
    __tablename__ = "branch_rules"
    
    id = Column(Integer, primary_key=True, index=True)
    branch_pattern = Column(String, unique=True, nullable=False)  # e.g., "feature/*"
    description = Column(String, nullable=False)
    expectations = Column(JSON, nullable=False)  # Rules for this branch type
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())