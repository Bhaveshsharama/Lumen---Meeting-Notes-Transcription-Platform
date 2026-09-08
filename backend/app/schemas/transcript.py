from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class TranscriptPaste(BaseModel):
    text: str
    format: str = Field(..., pattern="^(txt|vtt|json)$")

class SegmentUpdate(BaseModel):
    text: Optional[str] = None
    speaker_id: Optional[str] = None

class TranscriptSegmentResponse(BaseModel):
    id: int
    meeting_id: int
    sequence: int
    start_time: float
    end_time: float
    speaker_id: Optional[int] = None
    speaker_label: Optional[str] = None
    text: str
    
    model_config = ConfigDict(from_attributes=True)
