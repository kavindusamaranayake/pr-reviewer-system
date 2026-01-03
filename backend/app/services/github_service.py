from github import Github
from typing import Optional

class GitHubService:
    
    def __init__(self, token: str):
        self.github = Github(token)
    
    def post_review_comment(
        self, 
        repo_full_name: str, 
        pr_number: int, 
        comment_body: str,
        commit_sha: str
    ) -> bool:
        """Post a review comment to a PR"""
        try:
            repo = self.github.get_repo(repo_full_name)
            pr = repo.get_pull(pr_number)
            
            # Post as a review comment
            pr.create_issue_comment(comment_body)
            
            return True
        except Exception as e:
            print(f"Error posting comment: {e}")
            return False
    
    def merge_pull_request(
        self,
        repo_full_name: str,
        pr_number: int,
        commit_message: Optional[str] = None,
        merge_method: str = "merge"  # "merge", "squash", or "rebase"
    ) -> dict:
        """
        Merge a pull request
        
        Args:
            repo_full_name: Full repository name (owner/repo)
            pr_number: Pull request number
            commit_message: Optional custom merge commit message
            merge_method: Merge method - "merge", "squash", or "rebase"
            
        Returns:
            dict with success status and message
        """
        try:
            repo = self.github.get_repo(repo_full_name)
            pr = repo.get_pull(pr_number)
            
            # Check if PR is mergeable
            if pr.mergeable is False:
                return {
                    "success": False,
                    "message": "PR has merge conflicts and cannot be merged",
                    "merged": False
                }
            
            if pr.merged:
                return {
                    "success": False,
                    "message": "PR is already merged",
                    "merged": True
                }
            
            # Default merge message
            if not commit_message:
                commit_message = f"Merge PR #{pr_number}: {pr.title}"
            
            # Merge the PR
            result = pr.merge(
                commit_message=commit_message,
                merge_method=merge_method
            )
            
            if result.merged:
                return {
                    "success": True,
                    "message": f"PR #{pr_number} merged successfully",
                    "merged": True,
                    "sha": result.sha
                }
            else:
                return {
                    "success": False,
                    "message": "Failed to merge PR",
                    "merged": False
                }
                
        except Exception as e:
            print(f"Error merging PR: {e}")
            return {
                "success": False,
                "message": f"Error: {str(e)}",
                "merged": False
            }
    
    def check_pr_status(
        self,
        repo_full_name: str,
        pr_number: int
    ) -> dict:
        """
        Check PR status and mergeability
        
        Returns:
            dict with PR status information
        """
        try:
            repo = self.github.get_repo(repo_full_name)
            pr = repo.get_pull(pr_number)
            
            # Get required status checks
            branch_protection = None
            required_checks = []
            
            try:
                branch_protection = repo.get_branch(pr.base.ref).get_protection()
                if branch_protection.required_status_checks:
                    required_checks = branch_protection.required_status_checks.contexts
            except:
                pass  # Branch protection might not be enabled
            
            # Get commit status
            commit = repo.get_commit(pr.head.sha)
            commit_status = commit.get_combined_status()
            
            return {
                "mergeable": pr.mergeable,
                "merged": pr.merged,
                "state": pr.state,  # "open" or "closed"
                "mergeable_state": pr.mergeable_state,  # "clean", "unstable", "dirty", etc.
                "status_checks": {
                    "state": commit_status.state,  # "success", "pending", "failure"
                    "statuses": [
                        {
                            "context": status.context,
                            "state": status.state
                        }
                        for status in commit_status.statuses
                    ]
                },
                "required_checks": required_checks,
                "can_merge": pr.mergeable and commit_status.state in ["success", ""]
            }
            
        except Exception as e:
            print(f"Error checking PR status: {e}")
            return {
                "mergeable": False,
                "error": str(e)
            }
    
    def get_pr_info(self, repo_full_name: str, pr_number: int):
        """Get PR information"""
        repo = self.github.get_repo(repo_full_name)
        pr = repo.get_pull(pr_number)
        return pr






# from github import Github

# from typing import Optional

# class GitHubService:
    
#     def __init__(self, token: str):
#         self.github = Github(token)
    
#     def post_review_comment(
#         self, 
#         repo_full_name: str, 
#         pr_number: int, 
#         comment_body: str,
#         commit_sha: str
#     ) -> bool:
#         """Post a review comment to a PR"""
#         try:
#             repo = self.github.get_repo(repo_full_name)
#             pr = repo.get_pull(pr_number)  
            
#             # Post as a review comment
#             pr.create_issue_comment(comment_body)
            
#             return True
#         except Exception as e:
#             print(f"Error posting comment: {e}")
#             return False
    
#     def get_pr_info(self, repo_full_name: str, pr_number: int):
#         """Get PR information"""
#         repo = self.github.get_repo(repo_full_name)
#         pr = repo.get_pull(pr_number)  
#         return pr