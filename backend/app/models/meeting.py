"""
models/meeting.py — Meeting ORM model.

SRP: Maps exclusively to the `meetings` table. This is the core entity for
the dashboard — title, date, duration, media, tags, status all live here.

Design notes:
- media_type CHECK constraint ('audio', 'video') enforced at DB level.
- status CHECK constraint ('processing', 'ready', 'failed') enforced at DB level.
- tags stored as comma-separated text (simple at this scale, upgrade path to
  join table documented in database_schema.md).
- Cascading relationships: deleting a meeting cascades to segments, summary,
  topics, action_items, and meeting_participant links (relies on PRAGMA
  foreign_keys=ON in session.py).
"""

from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Index, ForeignKey, CheckConstraint, JSON
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.base import Base


class Meeting(Base):
    __tablename__ = "meetings"
    __table_args__ = (
        CheckConstraint("media_type IN ('audio', 'video')", name="ck_meeting_media_type"),
        CheckConstraint("status IN ('processing', 'ready', 'failed')", name="ck_meeting_status"),
        Index("idx_meetings_date", "meeting_date"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    meeting_date = Column(DateTime, nullable=False)
    duration_seconds = Column(Integer, nullable=False, default=0)
    media_url = Column(Text, nullable=True)
    media_type = Column(String, nullable=True, default="audio")
    tags = Column(JSON, nullable=True)
    status = Column(String, nullable=False, default="ready")
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # --- Relationships ---
    owner = relationship("User", back_populates="meetings")

    # Many-to-many with participants via MeetingParticipant
    participant_links = relationship(
        "MeetingParticipant", back_populates="meeting", cascade="all, delete-orphan"
    )

    # One-to-many: a meeting has many transcript segments
    segments = relationship(
        "TranscriptSegment", back_populates="meeting", cascade="all, delete-orphan",
        order_by="TranscriptSegment.sequence"
    )

    # One-to-one: a meeting has at most one summary
    summary = relationship(
        "Summary", back_populates="meeting", uselist=False, cascade="all, delete-orphan"
    )

    # One-to-many: a meeting has many topics (outline/chapters)
    topics = relationship(
        "Topic", back_populates="meeting", cascade="all, delete-orphan",
        order_by="Topic.sequence"
    )

    # One-to-many: a meeting has many action items
    action_items = relationship(
        "ActionItem", back_populates="meeting", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Meeting id={self.id} title={self.title!r}>"

    @property
    def summary_overview(self) -> str | None:
        return self.summary.overview if self.summary else None
