import subprocess, json, tempfile, os
 
def run_bandit(file_path: str, file_content: str):
    findings = []
    if not file_path.endswith(".py"):
        return findings
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as tmp:
        tmp.write(file_content)
        tmp_path = tmp.name
    try:
        result = subprocess.run(
            ["bandit", "-f", "json", tmp_path],
            capture_output=True, text=True,
        )
        data = json.loads(result.stdout or "{}")
        for issue in data.get("results", []):
            findings.append({
                "file_path": file_path,
                "line_number": issue["line_number"],
                "severity": issue["issue_severity"].lower(),
                "category": "security",
                "message": issue["issue_text"],
                "suggested_fix": None,
                "source": "static",
            })
    finally:
        os.unlink(tmp_path)
    return findings