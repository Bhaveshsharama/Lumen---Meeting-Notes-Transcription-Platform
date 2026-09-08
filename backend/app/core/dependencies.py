"""
core/dependencies.py — Dependency Injection setup utilizing FastAPI Depends.
"""
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Generator

from app.db.session import SessionLocal

# Repositories
from app.repositories.meeting_repository import MeetingRepository
from app.repositories.transcript_repository import TranscriptRepository
from app.repositories.summary_repository import SummaryRepository
from app.repositories.action_item_repository import ActionItemRepository

# Services
from app.services.meeting_service import MeetingService
from app.services.transcript_service import TranscriptService
from app.services.summary_service import SummaryService
from app.services.action_item_service import ActionItemService
from app.services.generators.llm_generator import LLMSummaryGenerator

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(db: Session = Depends(get_db)):
    from app.models.user import User
    # In a real app, this parses JWT. Here we return the default seed user.
    user = db.query(User).filter(User.email == "demo@fireflies-clone.local").first()
    if not user:
        # Fallback if seed wasn't run perfectly
        user = db.query(User).first()
    return user

# --- Repository Providers ---
def get_meeting_repo(db: Session = Depends(get_db)) -> MeetingRepository:
    return MeetingRepository(db)

def get_transcript_repo(db: Session = Depends(get_db)) -> TranscriptRepository:
    return TranscriptRepository(db)

def get_summary_repo(db: Session = Depends(get_db)) -> SummaryRepository:
    return SummaryRepository(db)

def get_action_item_repo(db: Session = Depends(get_db)) -> ActionItemRepository:
    return ActionItemRepository(db)


# --- Service Providers ---
def get_meeting_service(
    repo: MeetingRepository = Depends(get_meeting_repo),
    db: Session = Depends(get_db)
) -> MeetingService:
    return MeetingService(repo, db)

def get_transcript_service(
    repo: TranscriptRepository = Depends(get_transcript_repo),
    db: Session = Depends(get_db)
) -> TranscriptService:
    return TranscriptService(repo, db)

def get_summary_service(
    summary_repo: SummaryRepository = Depends(get_summary_repo),
    transcript_repo: TranscriptRepository = Depends(get_transcript_repo),
    action_item_repo: ActionItemRepository = Depends(get_action_item_repo),
    db: Session = Depends(get_db)
) -> SummaryService:
    # Factory for generator, injected into service
    generator = LLMSummaryGenerator()
    return SummaryService(summary_repo, transcript_repo, action_item_repo, generator, db)

def get_action_item_service(
    repo: ActionItemRepository = Depends(get_action_item_repo),
    db: Session = Depends(get_db)
) -> ActionItemService:
    return ActionItemService(repo, db)
