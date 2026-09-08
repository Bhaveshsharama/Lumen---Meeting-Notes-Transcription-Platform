from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from datetime import datetime

class SummaryGenerateRequest(BaseModel):
    source: str = Field(..., pattern="^(mock|llm)$")

class SummaryUpdate(BaseModel):
    overview: str

class TopicBase(BaseModel):
    title: str
    start_time: float

class TopicCreate(TopicBase):
    pass

class TopicUpdate(BaseModel):
    title: Optional[str] = None
    start_time: Optional[float] = None

class TopicResponse(TopicBase):
    id: int
    meeting_id: int
    model_config = ConfigDict(from_attributes=True)

class SummaryResponse(BaseModel):
    meeting_id: int
    overview: str
    generated_at: datetime
    
    topics: List[TopicResponse] = []
    
    model_config = ConfigDict(from_attributes=True)
