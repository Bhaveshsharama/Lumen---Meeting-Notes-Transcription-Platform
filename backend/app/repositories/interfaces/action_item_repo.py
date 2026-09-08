"""
repositories/interfaces/action_item_repo.py — ISP: Action Item operations.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from app.models import ActionItem

class IActionItemRepository(ABC):
    @abstractmethod
    def list_by_meeting(self, meeting_id: int, completed_filter: Optional[bool] = None) -> List[ActionItem]:
        """Lists action items for a meeting, optionally filtered by completed status."""
        pass

    @abstractmethod
    def create(self, data: Dict[str, Any]) -> ActionItem:
        """Creates a new action item."""
        pass

    @abstractmethod
    def update(self, action_item_id: int, data: Dict[str, Any]) -> ActionItem:
        """Updates an action item. Raises NotFoundError if not found."""
        pass

    @abstractmethod
    def delete(self, action_item_id: int) -> None:
        """Deletes an action item. Raises NotFoundError if not found."""
        pass
