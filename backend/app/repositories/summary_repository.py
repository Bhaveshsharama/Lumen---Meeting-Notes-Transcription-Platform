"""
repositories/summary_repository.py — concrete SQLAlchemy implementation for summaries and topics.
"""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models import Summary, Topic, Meeting
from app.repositories.interfaces.summary_repo import ISummaryRepository


class SummaryRepository(ISummaryRepository):
    def __init__(self, db: Session):
        self.db = db

    # --- Summary ---
    def get_by_meeting(self, meeting_id: int) -> Optional[Summary]:
        return self.db.query(Summary).filter(Summary.meeting_id == meeting_id).first()

    def upsert(self, meeting_id: int, overview: str) -> Summary:
        # Enforce meeting existence first
        meeting = self.db.query(Meeting).filter(Meeting.id == meeting_id).first()
        if not meeting:
            raise NotFoundError(f"Meeting with id {meeting_id} not found")

        # Select to see if exists
        existing = self.get_by_meeting(meeting_id)
        if existing:
            existing.overview = overview
            self.db.flush()
            return existing
        else:
            summary = Summary(meeting_id=meeting_id, overview=overview)
            self.db.add(summary)
            self.db.flush()
            return summary

    # --- Topics ---
    def list_topics(self, meeting_id: int) -> List[Topic]:
        return self.db.query(Topic)\
            .filter(Topic.meeting_id == meeting_id)\
            .order_by(Topic.sequence)\
            .all()

    def create_topic(self, meeting_id: int, data: Dict[str, Any]) -> Topic:
        meeting = self.db.query(Meeting).filter(Meeting.id == meeting_id).first()
        if not meeting:
            raise NotFoundError(f"Meeting with id {meeting_id} not found")

        # Auto-sequence calculation if not provided
        if "sequence" not in data:
            last_topic = self.db.query(Topic)\
                .filter(Topic.meeting_id == meeting_id)\
                .order_by(Topic.sequence.desc())\
                .first()
            data["sequence"] = (last_topic.sequence + 1) if last_topic else 1

        topic = Topic(meeting_id=meeting_id, **data)
        self.db.add(topic)
        self.db.flush()
        return topic

    def update_topic(self, topic_id: int, data: Dict[str, Any]) -> Topic:
        topic = self.db.query(Topic).filter(Topic.id == topic_id).first()
        if not topic:
            raise NotFoundError(f"Topic with id {topic_id} not found")
            
        for key, value in data.items():
            setattr(topic, key, value)
            
        self.db.flush()
        return topic

    def delete_topic(self, topic_id: int) -> None:
        topic = self.db.query(Topic).filter(Topic.id == topic_id).first()
        if not topic:
            raise NotFoundError(f"Topic with id {topic_id} not found")
            
        self.db.delete(topic)
        self.db.flush()
