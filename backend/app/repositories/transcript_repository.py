"""
repositories/transcript_repository.py — concrete SQLAlchemy implementation for transcripts and annotations.
"""
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models import TranscriptSegment, Annotation
from app.repositories.interfaces.transcript_repo import ITranscriptRepository

class TranscriptRepository(ITranscriptRepository):
    def __init__(self, db: Session):
        self.db = db

    # --- Segments ---
    def get_by_meeting(self, meeting_id: int) -> List[TranscriptSegment]:
        return self.db.query(TranscriptSegment).filter(
            TranscriptSegment.meeting_id == meeting_id
        ).order_by(TranscriptSegment.sequence).all()

    def replace_segments(self, meeting_id: int, segments_data: List[Dict[str, Any]]) -> List[TranscriptSegment]:
        # Delete old segments first
        self.db.query(TranscriptSegment).filter(TranscriptSegment.meeting_id == meeting_id).delete()
        
        segments = []
        for data in segments_data:
            data = dict(data)  # copy so we don't mutate source
            data["meeting_id"] = meeting_id
            # Parser returns speaker_id as a plain string (e.g. 'Alice').
            # Remap it to speaker_label (Text) to avoid the FK constraint on participants.
            speaker_label = data.pop("speaker_id", None)
            data["speaker_label"] = speaker_label
            segments.append(TranscriptSegment(**data))
        
        self.db.add_all(segments)
        self.db.flush()
        
        return self.get_by_meeting(meeting_id)

    def search_segments(self, meeting_id: int, query: str) -> List[TranscriptSegment]:
        term = f"%{query}%"
        return self.db.query(TranscriptSegment).filter(
            TranscriptSegment.meeting_id == meeting_id,
            TranscriptSegment.text.ilike(term)
        ).order_by(TranscriptSegment.start_time).all()

    def update(self, segment_id: int, data: Dict[str, Any]) -> TranscriptSegment:
        segment = self.db.query(TranscriptSegment).filter(TranscriptSegment.id == segment_id).first()
        if not segment:
            raise NotFoundError(f"TranscriptSegment with id {segment_id} not found")
            
        for key, value in data.items():
            setattr(segment, key, value)
        
        self.db.flush()
        return segment

    # --- Annotations ---
    def list_annotations(self, meeting_id: int) -> List[Annotation]:
        # Join allows filtering by meeting_id on the segment
        return self.db.query(Annotation)\
            .join(TranscriptSegment)\
            .filter(TranscriptSegment.meeting_id == meeting_id)\
            .all()

    def create_annotation(self, segment_id: int, data: Dict[str, Any]) -> Annotation:
        segment = self.db.query(TranscriptSegment).filter(TranscriptSegment.id == segment_id).first()
        if not segment:
            raise NotFoundError(f"TranscriptSegment with id {segment_id} not found")

        annotation = Annotation(segment_id=segment_id, **data)
        self.db.add(annotation)
        self.db.flush()
        return annotation

    def delete_annotation(self, annotation_id: int) -> None:
        annotation = self.db.query(Annotation).filter(Annotation.id == annotation_id).first()
        if not annotation:
            raise NotFoundError(f"Annotation with id {annotation_id} not found")
        
        self.db.delete(annotation)
        self.db.flush()
