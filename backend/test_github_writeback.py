from app.github_client import build_summary


findings = [
    {
        "file_path": "test.py",
        "line_number": 2,
        "severity": "high",
        "category": "security",
        "message": "Possible hardcoded password",
        "suggested_fix": None,
        "source": "static",
    },
    {
        "file_path": "test.py",
        "line_number": 5,
        "severity": "medium",
        "category": "logic",
        "message": "Possible logic issue",
        "suggested_fix": None,
        "source": "llm",
    },
    {
        "file_path": "main.py",
        "line_number": 10,
        "severity": "low",
        "category": "style",
        "message": "Style issue",
        "suggested_fix": None,
        "source": "llm",
    },
]


summary = build_summary(findings)

print(summary)