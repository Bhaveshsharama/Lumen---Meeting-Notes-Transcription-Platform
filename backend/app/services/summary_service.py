"""
services/summary_service.py — Orchestrates AI summary logic.

DIP: Passes 3 different repository interfaces and a generator interface.
SRP: The generator strictly returns data, and this service manages saving it.
"""
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from app.models import Summary, Topic
from app.repositories.interfaces.summary_repo import ISummaryRepository
from app.repositories.interfaces.transcript_repo import ITranscriptRepository
from app.repositories.interfaces.action_item_repo import IActionItemRepository
from app.services.generators.base import SummaryGenerator
from app.core.exceptions import ValidationError

class SummaryService:
    def __init__(
        self, 
        summary_repo: ISummaryRepository, 
        transcript_repo: ITranscriptRepository,
        action_item_repo: IActionItemRepository,
        generator: SummaryGenerator,
        db: Session
    ):
        self.summary_repo = summary_repo
        self.transcript_repo = transcript_repo
        self.action_item_repo = action_item_repo
        self.generator = generator
        self.db = db

    def get_summary(self, meeting_id: int) -> Optional[Summary]:
        return self.summary_repo.get_by_meeting(meeting_id)

    def get_topics(self, meeting_id: int) -> List[Topic]:
        return self.summary_repo.list_topics(meeting_id)

    def generate_summary(self, meeting_id: int) -> Summary:
        """
        Orchestrates extracting the transcript, feeding the AI Generator, and 
        saving Overview, Topics, and Action Tasks in a single transaction.
        """
        segments = self.transcript_repo.get_by_meeting(meeting_id)
        if not segments:
            raise ValidationError("Please upload a transcript before summarizing.")
        
        # Combine text
        transcript_text = "\n".join([f"{s.speaker_id or 'Unknown'}: {s.text}" for s in segments])

        # Generator returns flat dictionary data (SRP)
        generated_data = self.generator.generate(transcript_text)

        try:
            # Save Summary Text
            summary = self.summary_repo.upsert(meeting_id, generated_data.get("overview", ""))

            # Sync the overview directly back to the Meeting.description for the dashboard list
            from app.models.meeting import Meeting
            meeting = self.db.query(Meeting).filter(Meeting.id == meeting_id).first()
            if meeting:
                meeting.description = generated_data.get("overview", "")

            # Wipe old topics and create new
            old_topics = self.summary_repo.list_topics(meeting_id)
            for old_topic in old_topics:
                self.summary_repo.delete_topic(old_topic.id)
            
            for t_data in generated_data.get("topics", []):
                self.summary_repo.create_topic(meeting_id, t_data)

            # Insert Action Items (Optional, we preserve manually added ones 
            # by strictly only appending new AI-discovered ones).
            for a_data in generated_data.get("action_items", []):
                a_data["meeting_id"] = meeting_id
                self.action_item_repo.create(a_data)

            self.db.commit()
            self.db.refresh(summary)
            return summary
            
        except Exception:
            self.db.rollback()
            raise

    # --- Direct Modifications ---
    def update_summary(self, meeting_id: int, overview: str) -> Summary:
        try:
            s = self.summary_repo.upsert(meeting_id, overview)
            self.db.commit()
            self.db.refresh(s)
            return s
        except Exception:
            self.db.rollback()
            raise

    def create_topic(self, meeting_id: int, data: Dict[str, Any]) -> Topic:
        try:
            t = self.summary_repo.create_topic(meeting_id, data)
            self.db.commit()
            self.db.refresh(t)
            return t
        except Exception:
            self.db.rollback()
            raise
            
    def update_topic(self, topic_id: int, data: Dict[str, Any]) -> Topic:
        try:
            t = self.summary_repo.update_topic(topic_id, data)
            self.db.commit()
            self.db.refresh(t)
            return t
        except Exception:
            self.db.rollback()
            raise

    def delete_topic(self, topic_id: int) -> None:
        try:
            self.summary_repo.delete_topic(topic_id)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
