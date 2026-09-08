"""
models/topic.py — Topic ORM model.

SRP: Maps exclusively to the `topics` table. Each topic represents an
outline/chapter entry for a meeting — clicking a topic jumps the media
player to its start_time (same seek pattern as transcript segments).
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    meeting_id = Column(
        Integer, ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False
    )
    title = Column(String, nullable=False)
    start_time = Column(Float, nullable=False)
    sequence = Column(Integer, nullable=False)

    # --- Relationship ---
    meeting = relationship("Meeting", back_populates="topics")

    def __repr__(self) -> str:
        return f"<Topic id={self.id} title={self.title!r}>"
