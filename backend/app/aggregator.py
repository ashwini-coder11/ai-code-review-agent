def aggregate_findings(static_findings: list, llm_findings: list) -> list:
    combined = static_findings + llm_findings
 
    # Simple dedupe: same file + same line + same category -> keep the
    # static one (more deterministic) and drop the LLM duplicate.
    seen = set()
    deduped = []
    severity_rank = {"high": 3, "medium": 2, "low": 1}
 
    # Sort so 'static' entries are processed first per key, giving them
    # priority when a duplicate is found.
    combined.sort(key=lambda f: 0 if f["source"] == "static" else 1)
 
    for f in combined:
        key = (f["file_path"], f.get("line_number"), f["category"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(f)
 
    deduped.sort(key=lambda f: severity_rank.get(f["severity"], 0), reverse=True)
    return deduped