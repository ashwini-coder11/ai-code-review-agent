# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Review
from app.schemas import ReviewOut, ReviewDetailOut
from app.background import process_review


router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.get("", response_model=list[ReviewOut])
def list_reviews(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    return (
        db.query(Review)
        .order_by(Review.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/{review_id}", response_model=ReviewDetailOut)
def get_review(review_id: str, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()

    if not review:
        raise HTTPException(
            status_code=404,
            detail="Review not found",
        )

    return review


@router.post("/trigger")
def trigger_review(
    background_tasks: BackgroundTasks,
    repo_name: str = Query(...),
    pr_number: int = Query(...),
):
    background_tasks.add_task(process_review, repo_name, pr_number)

    return {"status": "queued"}