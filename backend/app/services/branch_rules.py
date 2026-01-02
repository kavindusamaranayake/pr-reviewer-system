import re
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from ..models import BranchRule

class BranchRulesService:
    
    # Default rules for common branch patterns
    DEFAULT_RULES = {
        "feature/*": {
            "description": "Feature branches for new functionality",
            "expectations": {
                "min_description_length": 50,
                "require_tests": True,
                "max_files_changed": 20,
                "require_documentation": True,
                "code_quality_threshold": 0.7,
                "checks": [
                    "Code follows naming conventions",
                    "Includes unit tests",
                    "Documentation updated",
                    "No console.log or debug statements",
                    "Error handling implemented"
                ]
            }
        },
        "bugfix/*": {
            "description": "Bug fix branches",
            "expectations": {
                "min_description_length": 30,
                "require_tests": True,
                "max_files_changed": 10,
                "require_documentation": False,
                "code_quality_threshold": 0.8,
                "checks": [
                    "Bug description is clear",
                    "Includes regression test",
                    "Root cause identified",
                    "No unrelated changes"
                ]
            }
        },
        "hotfix/*": {
            "description": "Critical production fixes",
            "expectations": {
                "min_description_length": 40,
                "require_tests": True,
                "max_files_changed": 5,
                "require_documentation": True,
                "code_quality_threshold": 0.9,
                "checks": [
                    "Critical issue documented",
                    "Minimal code changes",
                    "Tested in production-like environment",
                    "Rollback plan documented"
                ]
            }
        },
        "docs/*": {
            "description": "Documentation updates",
            "expectations": {
                "min_description_length": 20,
                "require_tests": False,
                "max_files_changed": 15,
                "require_documentation": False,
                "code_quality_threshold": 0.5,
                "checks": [
                    "Documentation is clear",
                    "No broken links",
                    "Proper formatting"
                ]
            }
        }
    }
    
    def __init__(self, db: Session):
        self.db = db
        self._ensure_default_rules()
    
    def _ensure_default_rules(self):
        """Ensure default rules exist in database"""
        for pattern, data in self.DEFAULT_RULES.items():
            existing = self.db.query(BranchRule).filter(
                BranchRule.branch_pattern == pattern
            ).first()
            
            if not existing:
                rule = BranchRule(
                    branch_pattern=pattern,
                    description=data["description"],
                    expectations=data["expectations"]
                )
                self.db.add(rule)
        
        self.db.commit()
    
    def get_expectations_for_branch(self, branch_name: str) -> Dict[str, Any]:
        """Get expectations based on branch name"""
        rules = self.db.query(BranchRule).all()
        
        for rule in rules:
            pattern = rule.branch_pattern.replace("*", ".*")
            if re.match(f"^{pattern}$", branch_name):
                return {
                    "branch_type": rule.branch_pattern,
                    "description": rule.description,
                    **rule.expectations
                }
        
        # Default if no pattern matches
        return {
            "branch_type": "default",
            "description": "Default branch rules",
            "min_description_length": 30,
            "require_tests": False,
            "max_files_changed": 30,
            "require_documentation": False,
            "code_quality_threshold": 0.6,
            "checks": [
                "Code is readable",
                "No obvious errors"
            ]
        }
    
    def extract_branch_type(self, branch_name: str) -> str:
        """Extract branch type from branch name"""
        expectations = self.get_expectations_for_branch(branch_name)
        return expectations["branch_type"]