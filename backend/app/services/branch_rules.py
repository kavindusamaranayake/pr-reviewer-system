import re
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from ..models import BranchRule

class BranchRulesService:
    
    # Default rules for common branch patterns
    DEFAULT_RULES = {
        "main": {
            "description": "Main production branch - highest standards",
            "expectations": {
                "min_description_length": 100,
                "require_tests": True,
                "max_files_changed": 10,
                "require_documentation": True,
                "code_quality_threshold": 0.95,
                "checks": [
                    "All tests passing",
                    "Code reviewed by at least 2 developers",
                    "No breaking changes",
                    "Changelog updated",
                    "Version number bumped",
                    "Documentation complete",
                    "Performance tested",
                    "Security reviewed"
                ]
            }
        },
        "develop": {  
            "description": "Development integration branch - testing and integration focus",
            "expectations": {
                "min_description_length": 60,
                "require_tests": True,
                "max_files_changed": 25,
                "require_documentation": True,
                "code_quality_threshold": 0.85,
                "checks": [
                    "All unit tests passing",
                    "Integration tests included",
                    "No merge conflicts with main",
                    "Code follows project conventions",
                    "Breaking changes documented",
                    "Dependencies updated if needed",
                    "CI/CD pipeline passes"
                ]
            }
        },
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
            "description": "Critical production fixes - highest urgency",
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
                    "Rollback plan documented",
                    "Monitoring added"
                ]
            }
        },
        "release/*": {  # Release branches
            "description": "Release preparation branches",
            "expectations": {
                "min_description_length": 80,
                "require_tests": True,
                "max_files_changed": 15,
                "require_documentation": True,
                "code_quality_threshold": 0.9,
                "checks": [
                    "Version number updated",
                    "Changelog complete",
                    "All tests passing",
                    "Documentation reviewed",
                    "Migration scripts tested",
                    "Deployment plan ready"
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
                    "Proper formatting",
                    "Examples provided where needed"
                ]
            }
        },
        "default": {  # ← Fallback for unmatched branches
            "description": "Default rules for other branches",
            "expectations": {
                "min_description_length": 30,
                "require_tests": False,
                "max_files_changed": 30,
                "require_documentation": False,
                "code_quality_threshold": 0.6,
                "checks": [
                    "Code is readable",
                    "No obvious errors",
                    "Follows basic conventions"
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
        
        # Check for exact match first (main, develop)
        for rule in rules:
            if rule.branch_pattern == branch_name:
                return {
                    "branch_type": rule.branch_pattern,
                    "description": rule.description,
                    **rule.expectations
                }
        
        # Then check pattern matches (feature/*, bugfix/*, etc.)
        for rule in rules:
            if '*' in rule.branch_pattern:
                pattern = rule.branch_pattern.replace("*", ".*")
                if re.match(f"^{pattern}$", branch_name):
                    return {
                        "branch_type": rule.branch_pattern,
                        "description": rule.description,
                        **rule.expectations
                    }
        
        # Default if no pattern matches
        default_rule = next((r for r in rules if r.branch_pattern == "default"), None)
        if default_rule:
            return {
                "branch_type": "default",
                "description": default_rule.description,
                **default_rule.expectations
            }
        
        # Fallback
        return self.DEFAULT_RULES["default"]["expectations"]
    
    def extract_branch_type(self, branch_name: str) -> str:
        """Extract branch type from branch name"""
        expectations = self.get_expectations_for_branch(branch_name)
        return expectations["branch_type"]
    
    def get_all_branch_rules(self) -> list:
        """Get all branch rules for display/management"""
        return self.db.query(BranchRule).all()
    
    def create_custom_rule(self, pattern: str, description: str, expectations: Dict) -> BranchRule:
        """Create a custom branch rule"""
        rule = BranchRule(
            branch_pattern=pattern,
            description=description,
            expectations=expectations
        )
        self.db.add(rule)
        self.db.commit()
        return rule
    
    def update_rule(self, pattern: str, description: str, expectations: Dict) -> BranchRule:
        """Update an existing rule"""
        rule = self.db.query(BranchRule).filter(
            BranchRule.branch_pattern == pattern
        ).first()
        
        if rule:
            rule.description = description
            rule.expectations = expectations
            self.db.commit()
        
        return rule