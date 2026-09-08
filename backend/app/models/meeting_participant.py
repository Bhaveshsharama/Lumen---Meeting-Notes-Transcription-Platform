"""
models/meeting_participant.py — MeetingParticipant join-table ORM model.

SRP: Maps exclusively to the `meeting_participants` table. This is the
many-to-many link between meetings and participants, storing the `role`
(host/attendee) for each association.

Composite primary key: (meeting_id, participant_id) — a person can only
appear once per meeting.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

from app.models.base import Base


class MeetingParticipant(Base):
    __tablename__ = "meeting_participants"
    __table_args__ = (
        CheckConstraint("role IN ('host', 'attendee')", name="ck_mp_role"),
    )

    meeting_id = Column(
        Integer,
        ForeignKey("meetings.id", ondelete="CASCADE"),
        primary_key=True
    )
    participant_id = Column(
        Integer,
        ForeignKey("participants.id", ondelete="CASCADE"),
        primary_key=True
    )
    role = Column(String, nullable=False, default="attendee")

    # --- Relationships ---
    meeting = relationship("Meeting", back_populates="participant_links")
    participant = relationship("Participant", back_populates="meeting_links")

    def __repr__(self) -> str:
        return f"<MeetingParticipant meeting={self.meeting_id} participant={self.participant_id} role={self.role!r}>"
