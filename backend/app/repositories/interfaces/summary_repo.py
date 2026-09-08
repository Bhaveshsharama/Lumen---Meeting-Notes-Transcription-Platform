"""
repositories/interfaces/summary_repo.py — ISP: Summary and Topic operations.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from app.models import Summary, Topic

class ISummaryRepository(ABC):
    # --- Summary ---
    @abstractmethod
    def get_by_meeting(self, meeting_id: int) -> Optional[Summary]:
        """Returns the summary for a meeting, or None if it doesn't exist."""
        pass

    @abstractmethod
    def upsert(self, meeting_id: int, overview: str) -> Summary:
        """Inserts or updates a meeting's summary text."""
        pass

    # --- Topics ---
    @abstractmethod
    def list_topics(self, meeting_id: int) -> List[Topic]:
        """Lists all topics for a meeting, ordered by sequence."""
        pass

    @abstractmethod
    def create_topic(self, meeting_id: int, data: Dict[str, Any]) -> Topic:
        """Creates a new topic for a meeting."""
        pass

    @abstractmethod
    def update_topic(self, topic_id: int, data: Dict[str, Any]) -> Topic:
        """Updates a topic. Raises NotFoundError if not found."""
        pass

    @abstractmethod
    def delete_topic(self, topic_id: int) -> None:
        """Deletes a topic. Raises NotFoundError if not found."""
        pass
