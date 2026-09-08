"""
repositories/interfaces/transcript_repo.py — ISP: Transcript Segment and Annotation operations.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from app.models import TranscriptSegment, Annotation

class ITranscriptRepository(ABC):
    # --- Segments ---
    @abstractmethod
    def get_by_meeting(self, meeting_id: int) -> List[TranscriptSegment]:
        """Returns all transcript segments for a meeting, ordered by sequence."""
        pass

    @abstractmethod
    def replace_segments(self, meeting_id: int, segments_data: List[Dict[str, Any]]) -> List[TranscriptSegment]:
        """Replaces all transcript segments for a meeting with the new ones."""
        pass

    @abstractmethod
    def search_segments(self, meeting_id: int, query: str) -> List[TranscriptSegment]:
        """Searches transcript segments in the database using LIKE."""
        pass

    @abstractmethod
    def update(self, segment_id: int, data: Dict[str, Any]) -> TranscriptSegment:
        """Updates a segment (e.g. correcting text or speaker). Raises NotFoundError."""
        pass

    # --- Annotations ---
    @abstractmethod
    def list_annotations(self, meeting_id: int) -> List[Annotation]:
        """Lists all annotations across all segments in a given meeting."""
        pass

    @abstractmethod
    def create_annotation(self, segment_id: int, data: Dict[str, Any]) -> Annotation:
        """Creates an annotation on a segment."""
        pass

    @abstractmethod
    def delete_annotation(self, annotation_id: int) -> None:
        """Deletes an annotation. Raises NotFoundError if not found."""
        pass
