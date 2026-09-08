"""
repositories/interfaces/meeting_repo.py — ISP: Meeting and Participant operations.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from app.models import Meeting, Participant

class IMeetingRepository(ABC):
    # --- Meetings ---
    @abstractmethod
    def get(self, id: int) -> Meeting:
        """Returns meeting by ID. Raises NotFoundError if not found."""
        pass

    @abstractmethod
    def list(self, filters: Dict[str, Any]) -> tuple[List[Meeting], int]:
        """Returns list of meetings and total count."""
        pass

    @abstractmethod
    def create(self, data: Dict[str, Any]) -> Meeting:
        """Creates a new meeting."""
        pass

    @abstractmethod
    def update(self, id: int, data: Dict[str, Any]) -> Meeting:
        """Updates a meeting. Raises NotFoundError if not found."""
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        """Deletes a meeting by ID. Raises NotFoundError if not found."""
        pass

    # --- Participants ---
    @abstractmethod
    def list_participants(self, query: Optional[str] = None) -> List[Participant]:
        """Lists participants, optionally filtered by a search query."""
        pass

    @abstractmethod
    def create_participant(self, data: Dict[str, Any]) -> Participant:
        """Creates a new participant."""
        pass

    @abstractmethod
    def add_participant(self, meeting_id: int, participant_id: int, role: str) -> None:
        """Adds a participant to a meeting with a specific role."""
        pass

    @abstractmethod
    def remove_participant(self, meeting_id: int, participant_id: int) -> None:
        """Removes a participant from a meeting."""
        pass
