from fastapi import APIRouter, Depends, UploadFile, File, Form, status, Query
from typing import List, Optional
import os

from app.schemas.transcript import TranscriptSegmentResponse, SegmentUpdate, TranscriptPaste
from app.services.transcript_service import TranscriptService
from app.core.dependencies import get_transcript_service
from app.core.exceptions import ValidationError

router = APIRouter(tags=["transcripts"])

@router.post("/meetings/{id}/transcript/upload", response_model=List[TranscriptSegmentResponse])
async def upload_transcript(
    id: int, 
    file: UploadFile = File(...),
    service: TranscriptService = Depends(get_transcript_service)
):
    ext = os.path.splitext(file.filename)[1].lower().replace(".", "")
    if not ext:
        raise ValidationError("File must have a valid extension (.txt, .vtt, .json)")
        
    contents = await file.read()
    return service.ingest(id, contents, ext)

@router.post("/meetings/{id}/transcript/paste", response_model=List[TranscriptSegmentResponse])
def paste_transcript(
    id: int,
    data: TranscriptPaste,
    service: TranscriptService = Depends(get_transcript_service)
):
    contents = data.text.encode('utf-8')
    return service.ingest(id, contents, data.format)

@router.get("/meetings/{id}/transcript", response_model=List[TranscriptSegmentResponse])
def get_transcript(id: int, service: TranscriptService = Depends(get_transcript_service)):
    return service.get_transcript(id)

@router.get("/meetings/{id}/transcript/search", response_model=List[TranscriptSegmentResponse])
def search_in_meeting(
    id: int, 
    q: str = Query(...), 
    service: TranscriptService = Depends(get_transcript_service)
):
    return service.search_in_meeting(id, q)

@router.patch("/segments/{id}", response_model=TranscriptSegmentResponse)
def update_segment(
    id: int, 
    data: SegmentUpdate, 
    service: TranscriptService = Depends(get_transcript_service)
):
    return service.update_segment(id, data.model_dump(exclude_unset=True))
