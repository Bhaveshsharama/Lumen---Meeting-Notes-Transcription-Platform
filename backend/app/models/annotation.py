"""
models/annotation.py — Annotation ORM model.

SRP: Maps exclusively to the `annotations` table. Unifies comments,
highlights, and soundbites in one table with a `type` discriminator column
instead of three near-identical tables — simpler schema, same functionality.

Design note: Cascade deletes from transcript_segments — if a segment is
deleted (e.g. because its parent meeting was deleted), its annotations go too.
"""

from sqlalchemy import Column, Integer, Text, String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.models.base import Base


class Annotation(Base):
    __tablename__ = "annotations"
    __table_args__ = (
        CheckConstraint(
            "type IN ('comment', 'highlight', 'soundbite')",
            name="ck_annotation_type"
        ),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    segment_id = Column(
        Integer,
        ForeignKey("transcript_segments.id", ondelete="CASCADE"),
        nullable=False
    )
    type = Column(String, nullable=False)  # 'comment', 'highlight', 'soundbite'
    content = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    # --- Relationship ---
    segment = relationship("TranscriptSegment", back_populates="annotations")

    def __repr__(self) -> str:
        return f"<Annotation id={self.id} type={self.type!r}>"
