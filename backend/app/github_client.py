# pyrefly: ignore [missing-import]
from github import Github
from app.config import settings
 
gh = Github(settings.GITHUB_TOKEN)
 
def get_pr_diff_files(repo_name: str, pr_number: int):
    repo = gh.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    files = []
    for f in pr.get_files():
        files.append({
            "filename": f.filename,
            "status": f.status,          # added/modified/removed
            "patch": f.patch,             # unified diff text (may be None for binaries)
            "additions": f.additions,
            "deletions": f.deletions,
        })
    return pr, files
 
def post_review_comments(repo_name: str, pr_number: int, summary: str, inline_comments: list):
    repo = gh.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    commit = pr.get_commits().reversed[0]
    comments = []
    for c in inline_comments:
        comments.append({
            "path": c["file_path"],
            "line": c["line_number"],
            "body": c["message"],
        })
    pr.create_review(commit=commit, body=summary, event="COMMENT", comments=comments)

def build_summary(findings: list) -> str:
    high = sum(1 for f in findings if f["severity"] == "high")
    medium = sum(1 for f in findings if f["severity"] == "medium")
    low = sum(1 for f in findings if f["severity"] == "low")
    static_n = sum(1 for f in findings if f["source"] == "static")
    llm_n = sum(1 for f in findings if f["source"] == "llm")

    return (
        f"**AI Code Review Summary**\n\n"
        f"Found {len(findings)} issue(s): {high} high, {medium} medium, {low} low.\n"
        f"Source split: {static_n} static, {llm_n} LLM-based.\n"
    )