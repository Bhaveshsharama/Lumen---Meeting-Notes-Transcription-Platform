"""
models/__init__.py — Re-exports all ORM models for convenient imports.

Usage: `from app.models import User, Meeting, ...`
Also ensures all models are registered with Base.metadata when this package
is imported (required by session.create_tables()).
"""

from app.models.base import Base
from app.models.user import User
from app.models.participant import Participant
from app.models.meeting import Meeting
from app.models.meeting_participant import MeetingParticipant
from app.models.transcript_segment import TranscriptSegment
from app.models.summary import Summary
from app.models.topic import Topic
from app.models.action_item import ActionItem
from app.models.annotation import Annotation

__all__ = [
    "Base",
    "User",
    "Participant",
    "Meeting",
    "MeetingParticipant",
    "TranscriptSegment",
    "Summary",
    "Topic",
    "ActionItem",
    "Annotation",
]
