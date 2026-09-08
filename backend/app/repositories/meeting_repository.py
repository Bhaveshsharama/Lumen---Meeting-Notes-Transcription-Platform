"""
repositories/meeting_repository.py — concrete SQLAlchemy implementation for meetings and participants.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_

from app.core.exceptions import NotFoundError
from app.models import Meeting, Participant, MeetingParticipant
from app.repositories.interfaces.meeting_repo import IMeetingRepository

class MeetingRepository(IMeetingRepository):
    def __init__(self, db: Session):
        self.db = db

    # --- Meetings ---
    def get(self, id: int) -> Meeting:
        meeting = (
            self.db.query(Meeting)
            .options(joinedload(Meeting.summary), joinedload(Meeting.participant_links))
            .filter(Meeting.id == id)
            .first()
        )
        if not meeting:
            raise NotFoundError(f"Meeting with id {id} not found")
        return meeting

    def list(self, filters: Dict[str, Any]) -> tuple[List[Meeting], int]:
        query = self.db.query(Meeting)
        
        # Search filter
        if filters.get("q"):
            term = f"%{filters['q']}%"
            query = query.filter(Meeting.title.ilike(term))
            
        if filters.get("owner_id"):
            query = query.filter(Meeting.owner_id == filters["owner_id"])

        # Participant filter — join through MeetingParticipant
        if filters.get("participant_id"):
            query = query.join(MeetingParticipant).filter(
                MeetingParticipant.participant_id == filters["participant_id"]
            )

        # Tag filter — SQLite JSON contains via LIKE on serialised column
        if filters.get("tag"):
            query = query.filter(Meeting.tags.ilike(f'%"{filters["tag"]}"%'))

        if filters.get("date_from"):
            query = query.filter(Meeting.meeting_date >= filters["date_from"])
            
        if filters.get("date_to"):
            query = query.filter(Meeting.meeting_date <= filters["date_to"])

        # Sort
        sort = filters.get("sort", "recent")
        if sort == "recent":
            query = query.order_by(Meeting.meeting_date.desc())
        else:
            query = query.order_by(Meeting.meeting_date.asc())

        # Total count BEFORE pagination
        total = query.count()

        # DB-level pagination
        page = filters.get("page", 1)
        page_size = filters.get("page_size", 20)
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)
        
        # Eagerly load summary so summary_overview property works during serialization
        meetings = (
            query.options(
                joinedload(Meeting.summary),
                joinedload(Meeting.participant_links)
            ).all()
        )
        return meetings, total

    def create(self, data: Dict[str, Any]) -> Meeting:
        meeting = Meeting(**data)
        self.db.add(meeting)
        self.db.flush()
        return meeting

    def update(self, id: int, data: Dict[str, Any]) -> Meeting:
        meeting = self.get(id)
        for key, value in data.items():
            setattr(meeting, key, value)
        self.db.flush()
        return meeting

    def delete(self, id: int) -> None:
        meeting = self.get(id)
        self.db.delete(meeting)
        self.db.flush()

    # --- Participants ---
    def list_participants(self, query_str: Optional[str] = None) -> List[Participant]:
        query = self.db.query(Participant)
        if query_str:
            term = f"%{query_str}%"
            query = query.filter(
                or_(Participant.name.ilike(term), Participant.email.ilike(term))
            )
        return query.all()

    def create_participant(self, data: Dict[str, Any]) -> Participant:
        if "email" in data and data["email"]:
            existing = self.db.query(Participant).filter(Participant.email == data["email"]).first()
            if existing:
                return existing

        participant = Participant(**data)
        self.db.add(participant)
        self.db.flush()
        return participant

    def add_participant(self, meeting_id: int, participant_id: int, role: str) -> None:
        self.get(meeting_id) 
        participant = self.db.query(Participant).filter(Participant.id == participant_id).first()
        if not participant:
            raise NotFoundError(f"Participant with id {participant_id} not found")
        
        mp = MeetingParticipant(meeting_id=meeting_id, participant_id=participant_id, role=role)
        self.db.merge(mp)
        self.db.flush()

    def remove_participant(self, meeting_id: int, participant_id: int) -> None:
        mp = self.db.query(MeetingParticipant).filter(
            MeetingParticipant.meeting_id == meeting_id,
            MeetingParticipant.participant_id == participant_id
        ).first()
        
        if not mp:
            raise NotFoundError("Participant is not in this meeting")
            
        self.db.delete(mp)
        self.db.flush()
