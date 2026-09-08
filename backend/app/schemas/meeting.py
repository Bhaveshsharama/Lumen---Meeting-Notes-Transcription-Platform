from pydantic import BaseModel, ConfigDict, field_validator
from typing import List, Optional
from datetime import date, datetime

class ParticipantBase(BaseModel):
    name: str
    email: Optional[str] = None
    avatar_url: Optional[str] = None

class ParticipantResponse(ParticipantBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class MeetingCreate(BaseModel):
    title: str
    meeting_date: str  # Accept date string like '2026-09-08' from frontend
    description: Optional[str] = None
    tags: Optional[List[str]] = []
    participant_ids: Optional[List[int]] = []

class MeetingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    participant_ids: Optional[List[int]] = None

class MeetingParticipantResponse(BaseModel):
    participant: ParticipantResponse
    role: str
    model_config = ConfigDict(from_attributes=True)

class MeetingResponse(BaseModel):
    id: int
    title: str
    meeting_date: datetime
    description: Optional[str] = None
    tags: Optional[List[str]] = []
    video_url: Optional[str] = None
    audio_url: Optional[str] = None
    duration_seconds: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    summary_overview: Optional[str] = None
    
    participant_links: List[MeetingParticipantResponse] = []
    
    @field_validator('tags', mode='before')
    @classmethod
    def parse_tags(cls, v):
        if not v:
            return []
        if isinstance(v, str):
            return [t.strip() for t in v.split(",") if t.strip()]
        if isinstance(v, list):
            return v
        return []
        
    model_config = ConfigDict(from_attributes=True)
