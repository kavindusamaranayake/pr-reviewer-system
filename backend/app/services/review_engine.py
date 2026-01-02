from typing import Dict, Any, List
from github import Github
import re

class ReviewEngine:
    
    def __init__(self, github_token: str):
        self.github = Github(github_token)
    
    def analyze_pr(
        self, 
        repo_full_name: str, 
        pr_number: int,
        expectations: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze a PR and generate structured feedback
        """
        repo = self.github.get_repo(repo_full_name)
        pr = repo.get_pull_request(pr_number)
        
        feedback_items = []
        
        # Check PR description length
        description_length = len(pr.body or "")
        min_length = expectations.get("min_description_length", 30)
        
        if description_length < min_length:
            feedback_items.append({
                "category": "Description",
                "severity": "warning",
                "message": f"PR description is too short ({description_length} chars). Expected at least {min_length} characters.",
                "line_number": None,
                "file_path": None
            })
        else:
            feedback_items.append({
                "category": "Description",
                "severity": "info",
                "message": "PR description meets length requirements.",
                "line_number": None,
                "file_path": None
            })
        
        # Check number of files changed
        files_changed = pr.changed_files
        max_files = expectations.get("max_files_changed", 30)
        
        if files_changed > max_files:
            feedback_items.append({
                "category": "Scope",
                "severity": "warning",
                "message": f"Too many files changed ({files_changed}). Consider breaking into smaller PRs. Maximum recommended: {max_files}",
                "line_number": None,
                "file_path": None
            })
        
        # Analyze changed files
        files = pr.get_files()
        
        test_files_found = False
        doc_files_found = False
        code_issues = []
        
        for file in files:
            filename = file.filename
            
            # Check for test files
            if 'test' in filename.lower() or 'spec' in filename.lower():
                test_files_found = True
            
            # Check for documentation
            if filename.endswith('.md') or 'readme' in filename.lower():
                doc_files_found = True
            
            # Analyze code content (basic checks)
            if file.patch:
                patch_content = file.patch
                
                # Check for console.log
                if 'console.log' in patch_content:
                    code_issues.append({
                        "category": "Code Quality",
                        "severity": "warning",
                        "message": "Found console.log statement. Remove debug code before merging.",
                        "file_path": filename
                    })
                
                # Check for TODO comments
                if 'TODO' in patch_content or 'FIXME' in patch_content:
                    code_issues.append({
                        "category": "Code Quality",
                        "severity": "info",
                        "message": "Found TODO/FIXME comment. Consider addressing before merge.",
                        "file_path": filename
                    })
                
                # Check for proper error handling (basic)
                if 'try' in patch_content.lower():
                    if 'except' not in patch_content.lower() and 'catch' not in patch_content.lower():
                        code_issues.append({
                            "category": "Error Handling",
                            "severity": "error",
                            "message": "Try block without proper error handling.",
                            "file_path": filename
                        })
        
        feedback_items.extend(code_issues)
        
        # Check for tests if required
        if expectations.get("require_tests", False):
            if not test_files_found:
                feedback_items.append({
                    "category": "Testing",
                    "severity": "error",
                    "message": "No test files found. Tests are required for this branch type.",
                    "line_number": None,
                    "file_path": None
                })
            else:
                feedback_items.append({
                    "category": "Testing",
                    "severity": "info",
                    "message": "Test files included ✓",
                    "line_number": None,
                    "file_path": None
                })
        
        # Check for documentation if required
        if expectations.get("require_documentation", False):
            if not doc_files_found:
                feedback_items.append({
                    "category": "Documentation",
                    "severity": "warning",
                    "message": "No documentation updates found. Consider updating relevant docs.",
                    "line_number": None,
                    "file_path": None
                })
        
        # Check against specific expectations
        for check in expectations.get("checks", []):
            feedback_items.append({
                "category": "Best Practices",
                "severity": "info",
                "message": f"Verify: {check}",
                "line_number": None,
                "file_path": None
            })
        
        # Generate summary
        error_count = sum(1 for item in feedback_items if item["severity"] == "error")
        warning_count = sum(1 for item in feedback_items if item["severity"] == "warning")
        
        summary = self._generate_summary(
            pr, 
            feedback_items, 
            error_count, 
            warning_count,
            expectations
        )
        
        return {
            "feedback_items": feedback_items,
            "summary": summary,
            "error_count": error_count,
            "warning_count": warning_count
        }
    
    def _generate_summary(
        self, 
        pr, 
        feedback_items: List[Dict], 
        error_count: int, 
        warning_count: int,
        expectations: Dict[str, Any]
    ) -> str:
        """Generate a human-readable summary"""
        
        summary_parts = [
            f"## Automated PR Review Summary\n",
            f"**PR:** {pr.title}",
            f"**Branch Type:** {expectations.get('branch_type', 'default')}",
            f"**Files Changed:** {pr.changed_files}",
            f"**Lines Added:** +{pr.additions} / **Lines Removed:** -{pr.deletions}\n",
            f"### Review Results",
            f"- ❌ **Errors:** {error_count}",
            f"- ⚠️  **Warnings:** {warning_count}",
            f"- ℹ️  **Info:** {len(feedback_items) - error_count - warning_count}\n",
        ]
        
        if error_count > 0:
            summary_parts.append("### 🔴 Critical Issues")
            for item in feedback_items:
                if item["severity"] == "error":
                    file_info = f" ({item['file_path']})" if item['file_path'] else ""
                    summary_parts.append(f"- {item['message']}{file_info}")
            summary_parts.append("")
        
        if warning_count > 0:
            summary_parts.append("### ⚠️ Warnings")
            for item in feedback_items:
                if item["severity"] == "warning":
                    file_info = f" ({item['file_path']})" if item['file_path'] else ""
                    summary_parts.append(f"- {item['message']}{file_info}")
            summary_parts.append("")
        
        summary_parts.append("### 📋 Branch-Specific Requirements")
        summary_parts.append(f"_{expectations.get('description', 'Default requirements')}_\n")
        
        if error_count == 0:
            summary_parts.append("✅ **This PR is ready for instructor review!**")
        else:
            summary_parts.append("⏸️ **Please address the errors before instructor review.**")
        
        return "\n".join(summary_parts)