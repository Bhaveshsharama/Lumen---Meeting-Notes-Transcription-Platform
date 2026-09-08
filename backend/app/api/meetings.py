from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional, Any, Dict
from pydantic import BaseModel
from datetime import datetime

from app.schemas.meeting import MeetingCreate, MeetingUpdate, MeetingResponse, ParticipantResponse, ParticipantBase
from app.services.meeting_service import MeetingService
from app.core.dependencies import get_meeting_service, get_current_user
from app.models.user import User

router = APIRouter(tags=["meetings"])

class PaginatedMeetingResponse(BaseModel):
    items: List[MeetingResponse]
    total: int
    page: int
    page_size: int

@router.get("/meetings", response_model=PaginatedMeetingResponse)
def list_meetings(
    q: Optional[str] = Query(None, alias="q"),
    participant_id: Optional[int] = None,
    tag: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    sort: str = "recent",
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    service: MeetingService = Depends(get_meeting_service)
):
    filters = {
        "q": q,
        "participant_id": participant_id,
        "tag": tag,
        "date_from": date_from,
        "date_to": date_to,
        "sort": sort,
        "page": page,
        "page_size": page_size
    }
    # For a real app, the repo would return total count, we simulate here
    all_meetings = service.list_meetings(filters)
    # The repository written previously currently returns List[Meeting].
    # In a full ORM implementation, we would paginate in the DB.
    # We will simulate the wrapper.
    if isinstance(all_meetings, tuple):
        items, total = all_meetings
    else:
        items = all_meetings
        total = len(all_meetings)

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size
    }

@router.post("/meetings", response_model=MeetingResponse, status_code=status.HTTP_201_CREATED)
def create_meeting(
    data: MeetingCreate, 
    service: MeetingService = Depends(get_meeting_service),
    current_user: User = Depends(get_current_user)
):
    meeting_data = data.model_dump(exclude_unset=True)
    # Parse date string to datetime if needed (frontend sends '2026-09-08')
    if isinstance(meeting_data.get("meeting_date"), str):
        try:
            meeting_data["meeting_date"] = datetime.fromisoformat(meeting_data["meeting_date"])
        except ValueError:
            pass
    return service.create_meeting(meeting_data, owner_id=current_user.id)

@router.get("/meetings/{id}", response_model=MeetingResponse)
def get_meeting(id: int, service: MeetingService = Depends(get_meeting_service)):
    return service.get_meeting(id)

@router.patch("/meetings/{id}", response_model=MeetingResponse)
def update_meeting(id: int, data: MeetingUpdate, service: MeetingService = Depends(get_meeting_service)):
    return service.update_meeting(id, data.model_dump(exclude_unset=True))

@router.delete("/meetings/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_meeting(id: int, service: MeetingService = Depends(get_meeting_service)):
    service.delete_meeting(id)

@router.get("/participants", response_model=List[ParticipantResponse])
def list_participants(q: Optional[str] = None, service: MeetingService = Depends(get_meeting_service)):
    return service.list_participants(q)

from fastapi.responses import StreamingResponse
from app.services.pdf_service import PDFExportService

@router.get("/meetings/{meeting_id}/export/pdf")
def export_meeting_pdf(meeting_id: int, service: MeetingService = Depends(get_meeting_service)):
    from app.core.exceptions import NotFoundError
    from fastapi import HTTPException
    try:
        meeting = service.get_meeting(meeting_id)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Meeting not found")

    summary = meeting.summary
    action_items = meeting.action_items
    topics = meeting.topics
    
    pdf_buffer = PDFExportService.generate_meeting_pdf(meeting, summary, action_items, topics)
    filename = "".join([c if c.isalnum() else "_" for c in meeting.title]).strip("_")
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="Meeting_{filename[:30]}.pdf"'}
    )

