from datetime import datetime

from app.db import SessionLocal
from app.models import Review, Finding, ReviewStatus
from app.github_client import (
    get_pr_diff_files,
    post_review_comments,
    build_summary,
)
from app.static_checks.bandit_check import run_bandit
from app.static_checks.semgrep_check import run_semgrep
from app.static_checks.secret_scan import scan_for_secrets
from app.agent.graph import run_llm_review
from app.aggregator import aggregate_findings


def process_review(repo_name: str, pr_number: int):
    db = SessionLocal()
    review = None

    try:
        review = Review(
            repo_name=repo_name,
            pr_number=pr_number,
            status=ReviewStatus.processing,
        )

        db.add(review)
        db.commit()
        db.refresh(review)

        pr, files = get_pr_diff_files(repo_name, pr_number)

        static_findings = []

        for f in files:
            content = f.get("patch") or ""

            static_findings += run_bandit(
                f["filename"],
                content,
            )

            static_findings += run_semgrep(
                f["filename"],
                content,
            )

            static_findings += scan_for_secrets(
                f["filename"],
                content,
            )

        llm_findings = run_llm_review(files)

        llm_findings = [
            {
                "file_path": f["file"],
                "line_number": f["line"],
                "severity": f["severity"],
                "category": f["category"],
                "message": f["explanation"],
                "suggested_fix": f.get("suggested_fix"),
                "source": f["source"],
            }
            for f in llm_findings
        ]

        all_findings = aggregate_findings(
            static_findings,
            llm_findings,
        )

        for f in all_findings:
            db.add(
                Finding(
                    review_id=review.id,
                    **f,
                )
            )

        review.total_findings = len(all_findings)
        review.status = ReviewStatus.completed
        review.completed_at = datetime.utcnow()

        db.commit()

        summary = build_summary(all_findings)

        post_review_comments(
            repo_name,
            pr_number,
            summary,
            all_findings,
        )

    except Exception:
        db.rollback()

        if review is not None:
            review.status = ReviewStatus.failed
            db.commit()

        raise

    finally:
        db.close()