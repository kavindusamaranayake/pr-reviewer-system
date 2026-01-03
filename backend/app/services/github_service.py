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
    
    def get_pr_info(self, repo_full_name: str, pr_number: int):
        """Get PR information"""
        repo = self.github.get_repo(repo_full_name)
        pr = repo.get_pull(pr_number)  
        return pr