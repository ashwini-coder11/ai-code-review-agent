import subprocess, json, tempfile, os
 
def run_semgrep(file_path: str, file_content: str):
    findings = []
    suffix = os.path.splitext(file_path)[1] or ".txt"
    with tempfile.NamedTemporaryFile(suffix=suffix, mode="w", delete=False) as tmp:
        tmp.write(file_content)
        tmp_path = tmp.name
    try:
        result = subprocess.run(
            ["semgrep", "--config=auto", "--json", tmp_path],
            capture_output=True, text=True,
        )
        data = json.loads(result.stdout or "{}")
        for r in data.get("results", []):
            findings.append({
                "file_path": file_path,
                "line_number": r["start"]["line"],
                "severity": r.get("extra", {}).get("severity", "medium").lower(),
                "category": "style",
                "message": r.get("extra", {}).get("message", "Semgrep finding"),
                "suggested_fix": None,
                "source": "static",
            })
    finally:
        os.unlink(tmp_path)
    return findings