from app.aggregator import aggregate_findings


static_findings = [
    {
        "file_path": "app.py",
        "line_number": 10,
        "severity": "high",
        "category": "security",
        "message": "Static security issue",
        "source": "static",
    },
    {
        "file_path": "utils.py",
        "line_number": 5,
        "severity": "low",
        "category": "style",
        "message": "Static style issue",
        "source": "static",
    },
]


llm_findings = [
    {
        "file_path": "app.py",
        "line_number": 10,
        "severity": "high",
        "category": "security",
        "message": "LLM found the same issue",
        "source": "llm",
    },
    {
        "file_path": "service.py",
        "line_number": 20,
        "severity": "medium",
        "category": "logic",
        "message": "LLM logic issue",
        "source": "llm",
    },
]


result = aggregate_findings(static_findings, llm_findings)

for finding in result:
    print(finding)