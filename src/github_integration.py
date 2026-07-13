import os
from github import Github
import logging
import uuid

logger = logging.getLogger(__name__)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO") # Format: "user/repo"
DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"

def create_remediation_pr(app_name, reason, proposed_fix, filepath_in_repo):
    """
    Simulates or performs creating a Pull Request via GitOps.
    In a real scenario, this would update the specific YAML file.
    """
    if DRY_RUN or not GITHUB_TOKEN or not GITHUB_REPO:
        logger.warning(f"Dry run or missing GitHub credentials. Skipping PR creation for {app_name}.")
        return "https://github.com/mock/repo/pull/mock"

    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(GITHUB_REPO)
        
        # 1. Get default branch and create a new branch
        base_branch = repo.default_branch
        ref = repo.get_git_ref(f"heads/{base_branch}")
        
        new_branch_name = f"auto-fix-{app_name}-{uuid.uuid4().hex[:6]}"
        repo.create_git_ref(ref=f"refs/heads/{new_branch_name}", sha=ref.object.sha)
        
        # 2. Update the file (mocking the YAML manipulation for demo purposes)
        # A real implementation would parse YAML, update (e.g., limits), and commit.
        file_contents = repo.get_contents(filepath_in_repo, ref=base_branch)
        content_str = file_contents.decoded_content.decode('utf-8')
        
        # Simple string replacement for demo (e.g., bumping memory from 256Mi to 512Mi)
        if "memory: 256Mi" in content_str:
            new_content = content_str.replace("memory: 256Mi", "memory: 512Mi")
        else:
            new_content = content_str + f"\n# Auto-updated by self-healing controller: {proposed_fix}\n"
        
        repo.update_file(
            path=filepath_in_repo,
            message=f"Automated Fix: {proposed_fix} for {app_name}",
            content=new_content,
            sha=file_contents.sha,
            branch=new_branch_name
        )
        
        # 3. Create PR
        pr = repo.create_pull(
            title=f"Automated Fix: {proposed_fix} for {app_name}",
            body=f"🚨 Incident detected due to: {reason}\n\nThis PR automatically applies the following fix: {proposed_fix}",
            head=new_branch_name,
            base=base_branch
        )
        
        logger.info(f"Created PR: {pr.html_url}")
        return pr.html_url
        
    except Exception as e:
        logger.error(f"Failed to create PR: {e}")
        return None
