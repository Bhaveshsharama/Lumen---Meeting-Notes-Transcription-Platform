"""
repositories/action_item_repository.py — concrete SQLAlchemy implementation for action items.
"""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models import ActionItem, Meeting
from app.repositories.interfaces.action_item_repo import IActionItemRepository

class ActionItemRepository(IActionItemRepository):
    def __init__(self, db: Session):
        self.db = db

    def list_by_meeting(self, meeting_id: int, completed_filter: Optional[bool] = None) -> List[ActionItem]:
        query = self.db.query(ActionItem).filter(ActionItem.meeting_id == meeting_id)
        if completed_filter is not None:
            query = query.filter(ActionItem.is_completed == completed_filter)
        return query.all()

    def create(self, data: Dict[str, Any]) -> ActionItem:
        meeting_id = data.get("meeting_id")
        meeting = self.db.query(Meeting).filter(Meeting.id == meeting_id).first()
        if not meeting:
            raise NotFoundError(f"Meeting with id {meeting_id} not found")
            
        item = ActionItem(**data)
        self.db.add(item)
        self.db.flush()
        return item

    def update(self, action_item_id: int, data: Dict[str, Any]) -> ActionItem:
        item = self.db.query(ActionItem).filter(ActionItem.id == action_item_id).first()
        if not item:
            raise NotFoundError(f"ActionItem with id {action_item_id} not found")
            
        for key, value in data.items():
            setattr(item, key, value)
            
        self.db.flush()
        return item

    def delete(self, action_item_id: int) -> None:
        item = self.db.query(ActionItem).filter(ActionItem.id == action_item_id).first()
        if not item:
            raise NotFoundError(f"ActionItem with id {action_item_id} not found")
            
        self.db.delete(item)
        self.db.flush()
