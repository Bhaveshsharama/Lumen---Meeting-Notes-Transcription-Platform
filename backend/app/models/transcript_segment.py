"""
models/transcript_segment.py — TranscriptSegment ORM model.

SRP: Maps exclusively to the `transcript_segments` table. One row per
spoken line in a meeting transcript.

Design notes:
- speaker_id FK uses ON DELETE SET NULL so deleting a participant doesn't
  destroy transcript data — the segment stays, just loses its speaker link.
- Unique constraint on (meeting_id, sequence) ensures no duplicate ordering.
- Index on (meeting_id, start_time) for efficient seek/search queries.
- This single table powers click-to-seek, seek-to-highlight, and in-meeting
  transcript search — all via start_time/end_time.
"""

from sqlalchemy import (
    Column, Integer, Float, Text, ForeignKey, UniqueConstraint, Index
)
from sqlalchemy.orm import relationship

from app.models.base import Base


class TranscriptSegment(Base):
    __tablename__ = "transcript_segments"
    __table_args__ = (
        UniqueConstraint("meeting_id", "sequence", name="uq_segment_meeting_seq"),
        Index("idx_segments_meeting_time", "meeting_id", "start_time"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    meeting_id = Column(
        Integer, ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False
    )
    speaker_id = Column(
        Integer, ForeignKey("participants.id", ondelete="SET NULL"), nullable=True
    )
    # Human-readable speaker label extracted from the transcript file (e.g. "Alice")
    speaker_label = Column(Text, nullable=True)
    sequence = Column(Integer, nullable=False)
    start_time = Column(Float, nullable=False)
    end_time = Column(Float, nullable=False)
    text = Column(Text, nullable=False)

    # --- Relationships ---
    meeting = relationship("Meeting", back_populates="segments")
    speaker = relationship("Participant", back_populates="segments")
    annotations = relationship(
        "Annotation", back_populates="segment", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<TranscriptSegment id={self.id} meeting={self.meeting_id} seq={self.sequence}>"
