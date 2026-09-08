from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ActionItemBase(BaseModel):
    text: str
    assignee_id: Optional[int] = None
    due_date: Optional[datetime] = None
    source_timestamp: Optional[float] = None

class ActionItemCreate(ActionItemBase):
    pass

class ActionItemUpdate(BaseModel):
    text: Optional[str] = None
    assignee_id: Optional[int] = None
    due_date: Optional[datetime] = None
    is_completed: Optional[bool] = None

class ActionItemResponse(ActionItemBase):
    id: int
    meeting_id: int
    is_completed: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
