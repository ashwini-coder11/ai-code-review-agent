import json
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from app.agent.prompts import REVIEW_SYSTEM_PROMPT
from app.config import settings


class ReviewState(TypedDict):
    files: List[dict]
    findings: List[dict]


llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    api_key=settings.GEMINI_API_KEY or "placeholder_key",
    temperature=0.2,
    max_output_tokens=4000,
)


def review_files_node(state: ReviewState) -> ReviewState:
    all_findings = []

    for f in state["files"]:
        if not f.get("patch"):
            continue

        prompt = f"File: {f['filename']}\n\nDiff:\n{f['patch']}"

        response = llm.invoke([
            {"role": "system", "content": REVIEW_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ])

        raw_content = response.content
        if isinstance(raw_content, list):
            parts = []
            for item in raw_content:
                if isinstance(item, str):
                    parts.append(item)
                elif isinstance(item, dict) and "text" in item:
                    parts.append(item["text"])
            raw_content = "".join(parts)

        raw_content_str = str(raw_content).strip()
        if raw_content_str.startswith("```"):
            lines = raw_content_str.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            raw_content_str = "\n".join(lines).strip()

        try:
            parsed = json.loads(raw_content_str)
            if isinstance(parsed, dict):
                parsed = [parsed]
        except (json.JSONDecodeError, TypeError):
            parsed = []

        for item in parsed:
            item["source"] = "llm"
            all_findings.append(item)

    state["findings"] = all_findings
    return state


graph = StateGraph(ReviewState)

graph.add_node("review_files", review_files_node)

graph.set_entry_point("review_files")

graph.add_edge("review_files", END)

review_graph = graph.compile()


def run_llm_review(files: list) -> list:
    result = review_graph.invoke({"files": files, "findings": []})
    return result["findings"]