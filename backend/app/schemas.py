# pyrefly: ignore [missing-import]
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime


class FindingOut(BaseModel):
    id: UUID
    file_path: str
    line_number: Optional[int]
    severity: str
    category: str
    message: str
    suggested_fix: Optional[str]
    source: str

    class Config:
        from_attributes = True


class ReviewOut(BaseModel):
    id: UUID
    pr_number: int
    repo_name: str
    created_at: datetime
    completed_at: Optional[datetime]
    total_findings: int
    status: str

    class Config:
        from_attributes = True


class ReviewDetailOut(ReviewOut):
    findings: List[FindingOut]