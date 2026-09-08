"""
services/transcript_service.py — Business logic for Transcripts.

DIP: Uses ITranscriptRepository.
OCP: Consumers ParserFactory to dynamically load parsing strategy.
"""
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from app.models import TranscriptSegment, Annotation
from app.repositories.interfaces.transcript_repo import ITranscriptRepository
from app.utils.transcript_parser.factory import ParserFactory

class TranscriptService:
    def __init__(self, repo: ITranscriptRepository, db: Session):
        self.repo = repo
        self.db = db

    def get_transcript(self, meeting_id: int) -> List[TranscriptSegment]:
        return self.repo.get_by_meeting(meeting_id)

    def ingest(self, meeting_id: int, file_bytes: bytes, format: str) -> List[TranscriptSegment]:
        """
        Parses transcript, and replaces old segments in a transaction.
        """
        # Pick concrete behavior matching OCP
        parser = ParserFactory.get_parser(format)
        segments_data = parser.parse(file_bytes)
        
        try:
            # Send to repo for segment replacement instead of generic bulk append
            segments = self.repo.replace_segments(meeting_id, segments_data)
            
            # Update meeting duration based on the last segment's end_time
            if segments:
                from app.models.meeting import Meeting
                meeting = self.db.query(Meeting).filter(Meeting.id == meeting_id).first()
                if meeting:
                    meeting.duration_seconds = int(segments[-1].end_time)
                    
            self.db.commit()
            return segments
        except Exception:
            self.db.rollback()
            raise

    def search_in_meeting(self, meeting_id: int, query: str) -> List[TranscriptSegment]:
        """Filters segments by a text phrase efficiently at the DB level."""
        return self.repo.search_segments(meeting_id, query)

    def update_segment(self, segment_id: int, data: Dict[str, Any]) -> TranscriptSegment:
        try:
            s = self.repo.update(segment_id, data)
            self.db.commit()
            self.db.refresh(s)
            return s
        except Exception:
            self.db.rollback()
            raise

    # --- Annotations ---
    def list_annotations(self, meeting_id: int) -> List[Annotation]:
        return self.repo.list_annotations(meeting_id)

    def create_annotation(self, segment_id: int, data: Dict[str, Any]) -> Annotation:
        try:
            a = self.repo.create_annotation(segment_id, data)
            self.db.commit()
            self.db.refresh(a)
            return a
        except Exception:
            self.db.rollback()
            raise

    def delete_annotation(self, annotation_id: int) -> None:
        try:
            self.repo.delete_annotation(annotation_id)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
