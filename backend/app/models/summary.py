"""
models/summary.py — Summary ORM model.

SRP: Maps exclusively to the `summaries` table. One row per meeting holding
the AI-generated overview text — split out from the meetings table so the
dashboard list query never has to load a potentially large text blob.

Design note: The primary key IS the meeting_id (also a FK) — this enforces
the one-to-one cardinality at the DB level. No separate auto-increment id.
"""

from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.models.base import Base


class Summary(Base):
    __tablename__ = "summaries"

    meeting_id = Column(
        Integer,
        ForeignKey("meetings.id", ondelete="CASCADE"),
        primary_key=True
    )
    overview = Column(Text, nullable=False)
    generated_at = Column(DateTime, nullable=False, server_default=func.now())

    # --- Relationships ---
    meeting = relationship("Meeting", back_populates="summary")

    def __repr__(self) -> str:
        return f"<Summary meeting_id={self.meeting_id}>"
