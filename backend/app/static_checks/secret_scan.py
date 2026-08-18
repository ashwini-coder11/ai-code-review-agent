import re
 
SECRET_PATTERNS = [
    (r"AKIA[0-9A-Z]{16}", "Possible AWS Access Key"),
    (r"sk-[a-zA-Z0-9]{20,}", "Possible API secret key"),
    (r"-----BEGIN PRIVATE KEY-----", "Possible private key committed"),
]
 
def scan_for_secrets(file_path: str, file_content: str):
    findings = []
    for pattern, label in SECRET_PATTERNS:
        for m in re.finditer(pattern, file_content):
            line_number = file_content[: m.start()].count("\n") + 1
            findings.append({
                "file_path": file_path,
                "line_number": line_number,
                "severity": "high",
                "category": "security",
                "message": label,
                "suggested_fix": "Remove secret and rotate the credential immediately.",
                "source": "static",
            })
    return findings