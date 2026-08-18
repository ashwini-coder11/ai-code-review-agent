def process_review(repo_name: str, pr_number: int):
    """
    Background task to process AI code review for a given GitHub pull request.
    """
    #print("BACKGROUND TASK STARTED")
    return {"repo_name": repo_name, "pr_number": pr_number, "status": "completed"}
