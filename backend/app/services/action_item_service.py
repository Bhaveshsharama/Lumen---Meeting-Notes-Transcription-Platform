"""
services/action_item_service.py — Business logic for Action Items.

DIP: Uses IActionItemRepository.
"""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.models import ActionItem
from app.repositories.interfaces.action_item_repo import IActionItemRepository

class ActionItemService:
    def __init__(self, repo: IActionItemRepository, db: Session):
        self.repo = repo
        self.db = db

    def list_items(self, meeting_id: int, completed: Optional[bool] = None) -> List[ActionItem]:
        return self.repo.list_by_meeting(meeting_id, completed)

    def create_item(self, meeting_id: int, data: Dict[str, Any]) -> ActionItem:
        data["meeting_id"] = meeting_id
        try:
            item = self.repo.create(data)
            self.db.commit()
            self.db.refresh(item)
            return item
        except Exception:
            self.db.rollback()
            raise

    def update_item(self, action_item_id: int, data: Dict[str, Any]) -> ActionItem:
        try:
            item = self.repo.update(action_item_id, data)
            self.db.commit()
            self.db.refresh(item)
            return item
        except Exception:
            self.db.rollback()
            raise

    def toggle_complete(self, action_item_id: int, is_completed: bool) -> ActionItem:
        try:
            item = self.repo.update(action_item_id, {"is_completed": is_completed})
            self.db.commit()
            self.db.refresh(item)
            return item
        except Exception:
            self.db.rollback()
            raise

    def delete_item(self, action_item_id: int) -> None:
        try:
            self.repo.delete(action_item_id)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
