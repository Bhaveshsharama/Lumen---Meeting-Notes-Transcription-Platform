"""
models/action_item.py — ActionItem ORM model.

SRP: Maps exclusively to the `action_items` table. Extracted tasks from a
meeting, each with an optional assignee (reuses participants table) and a
source_timestamp to jump back to the transcript moment it was mentioned.

Design note: assignee_id uses ON DELETE SET NULL — deleting a participant
doesn't destroy the task, it just unlinks the assignee.
"""

from sqlalchemy import Column, Integer, Text, Boolean, Date, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.models.base import Base


class ActionItem(Base):
    __tablename__ = "action_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    meeting_id = Column(
        Integer, ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False
    )
    assignee_id = Column(
        Integer, ForeignKey("participants.id", ondelete="SET NULL"), nullable=True
    )
    text = Column(Text, nullable=False)
    is_completed = Column(Boolean, nullable=False, default=False)
    due_date = Column(Date, nullable=True)
    source_timestamp = Column(Float, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    # --- Relationships ---
    meeting = relationship("Meeting", back_populates="action_items")
    assignee = relationship("Participant", back_populates="action_items")

    def __repr__(self) -> str:
        return f"<ActionItem id={self.id} text={self.text[:30]!r}>"
