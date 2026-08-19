from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Review, Finding


router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    total_reviews = db.query(func.count(Review.id)).scalar()
    total_findings = db.query(func.count(Finding.id)).scalar()

    severity_rows = (
        db.query(Finding.severity, func.count(Finding.id))
        .group_by(Finding.severity)
        .all()
    )

    category_rows = (
        db.query(Finding.category, func.count(Finding.id))
        .group_by(Finding.category)
        .all()
    )

    source_rows = (
        db.query(Finding.source, func.count(Finding.id))
        .group_by(Finding.source)
        .all()
    )

    return {
        "total_reviews": total_reviews,
        "total_findings": total_findings,
        "severity_breakdown": {
            s.value: c for s, c in severity_rows
        },
        "category_breakdown": {
            c_.value: c for c_, c in category_rows
        },
        "source_split": {
            s.value: c for s, c in source_rows
        },
    }


@router.get("/timeline")
def timeline(db: Session = Depends(get_db)):
    rows = (
        db.query(
            func.date(Review.created_at).label("day"),
            func.count(Review.id),
        )
        .group_by("day")
        .order_by("day")
        .all()
    )

    return [
        {"date": str(day), "count": count}
        for day, count in rows
    ]