import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
from app.db import Base
 
class ReviewStatus(str, enum.Enum):
    queued = "queued"
    processing = "processing"
    completed = "completed"
    failed = "failed"
 
class Severity(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
 
class Category(str, enum.Enum):
    security = "security"
    style = "style"
    logic = "logic"
    tests = "tests"
 
class Source(str, enum.Enum):
    static = "static"
    llm = "llm"
 
class Review(Base):
    __tablename__ = "reviews"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pr_number = Column(Integer, nullable=False)
    repo_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    total_findings = Column(Integer, default=0)
    status = Column(Enum(ReviewStatus), default=ReviewStatus.queued)
 
    findings = relationship("Finding", back_populates="review", cascade="all, delete-orphan")
 
class Finding(Base):
    __tablename__ = "findings"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    review_id = Column(UUID(as_uuid=True), ForeignKey("reviews.id"))
    file_path = Column(String, nullable=False)
    line_number = Column(Integer, nullable=True)
    severity = Column(Enum(Severity), nullable=False)
    category = Column(Enum(Category), nullable=False)
    message = Column(Text, nullable=False)
    suggested_fix = Column(Text, nullable=True)
    source = Column(Enum(Source), nullable=False)
 
    review = relationship("Review", back_populates="findings")