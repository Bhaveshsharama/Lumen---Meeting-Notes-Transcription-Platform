"""
services/meeting_service.py — Business logic for Meetings.

DIP: Employs IMeetingRepository instead of concrete class.
"""
from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session

from app.models import Meeting, Participant
from app.repositories.interfaces.meeting_repo import IMeetingRepository

class MeetingService:
    def __init__(self, repo: IMeetingRepository, db: Session):
        self.repo = repo
        self.db = db

    def get_meeting(self, meeting_id: int) -> Meeting:
        return self.repo.get(meeting_id)

    def list_meetings(self, filters: Dict[str, Any]) -> Tuple[List[Meeting], int]:
        return self.repo.list(filters)

    def create_meeting(self, data: Dict[str, Any], owner_id: int = None) -> Meeting:
        """
        Creates a meeting in a transaction. If meeting_participants are 
        supplied, adds them in the same transaction.
        """
        try:
            if owner_id is not None:
                data["owner_id"] = owner_id
                
            # Extract out relational data
            participant_ids = data.pop("participant_ids", [])
            
            # Create base meeting
            meeting = self.repo.create(data)

            # Link participants
            for p_id in participant_ids:
                self.repo.add_participant(meeting.id, p_id, "attendee")
            
            self.db.commit()
            self.db.refresh(meeting)
            return meeting
        except Exception:
            self.db.rollback()
            raise

    def update_meeting(self, meeting_id: int, data: Dict[str, Any]) -> Meeting:
        try:
            participant_ids = data.pop("participant_ids", None)
            meeting = self.repo.update(meeting_id, data)

            if participant_ids is not None:
                # Basic naive update logic: replace all for simplicity
                # Real logic might diff added/removed, but we just clear and add
                for mp in meeting.participant_links:
                    self.repo.remove_participant(meeting_id, mp.participant_id)
                for p_id in participant_ids:
                    self.repo.add_participant(meeting_id, p_id, "attendee")
            
            self.db.commit()
            self.db.refresh(meeting)
            return meeting
        except Exception:
            self.db.rollback()
            raise

    def delete_meeting(self, meeting_id: int) -> None:
        """
        Deletes the meeting ONLY. 
        Relies on ON DELETE CASCADE in SQLite to cleanup segments, summaries, 
        topics, and action items automatically.
        """
        try:
            self.repo.delete(meeting_id)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

    # --- Participants ---
    def list_participants(self, query: str = None) -> List[Participant]:
        return self.repo.list_participants(query)

    def create_participant(self, data: Dict[str, Any]) -> Participant:
        try:
            p = self.repo.create_participant(data)
            self.db.commit()
            self.db.refresh(p)
            return p
        except Exception:
            self.db.rollback()
            raise
