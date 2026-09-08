"""
models/participant.py — Participant ORM model.

SRP: Maps exclusively to the `participants` table. Participants are people
who attend meetings — they're their own entity (not free text) so the same
person can appear across multiple meetings via the meeting_participants
join table. This also lets action_items.assignee_id reference a real record.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base


class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)  # nullable per DDL

    # Many-to-many with meetings via MeetingParticipant
    meeting_links = relationship("MeetingParticipant", back_populates="participant")

    # Segments spoken by this participant
    segments = relationship("TranscriptSegment", back_populates="speaker")

    # Action items assigned to this participant
    action_items = relationship("ActionItem", back_populates="assignee")

    def __repr__(self) -> str:
        return f"<Participant id={self.id} name={self.name!r}>"
