import os
# pyrefly: ignore [missing-import]
from github import Github
from app.config import settings

gh = Github(settings.GITHUB_TOKEN)
try:
    print("Testing repo:", "ashwini-coder11/ai-code-review-test")
    repo = gh.get_repo("ashwini-coder11/ai-code-review-test")
    print("Repo:", repo.full_name)
    print("Fetching PR 1...")
    pr = repo.get_pull(1)
    print("PR:", pr.title)
except Exception as e:
    import traceback
    traceback.print_exc()
