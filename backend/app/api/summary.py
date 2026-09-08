from fastapi import APIRouter, Depends, status
from typing import List, Optional

from app.schemas.summary import (
    SummaryResponse, SummaryUpdate, SummaryGenerateRequest,
    TopicResponse, TopicCreate, TopicUpdate
)
from app.services.summary_service import SummaryService
from app.core.dependencies import get_summary_service

router = APIRouter(tags=["summaries"])

@router.get("/meetings/{id}/summary", response_model=SummaryResponse)
def get_summary(id: int, service: SummaryService = Depends(get_summary_service)):
    """Returns the summary text and topics together."""
    summary = service.get_summary(id)
    if not summary:
        from app.core.exceptions import NotFoundError
        raise NotFoundError("Summary not found")
        
    topics = service.get_topics(id)
    
    return {
        "meeting_id": summary.meeting_id,
        "overview": summary.overview,
        "generated_at": summary.generated_at,
        "topics": topics
    }

@router.post("/meetings/{id}/summary/generate", response_model=SummaryResponse)
def generate_summary(
    id: int, 
    data: SummaryGenerateRequest,
    service: SummaryService = Depends(get_summary_service)
):
    # Generator handles saving everything to DB
    summary = service.generate_summary(id)
    topics = service.get_topics(id)
    
    return {
        "meeting_id": summary.meeting_id,
        "overview": summary.overview,
        "generated_at": summary.generated_at,
        "topics": topics
    }

@router.patch("/meetings/{id}/summary", response_model=SummaryResponse)
def update_summary(
    id: int, 
    data: SummaryUpdate, 
    service: SummaryService = Depends(get_summary_service)
):
    return service.update_summary(id, data.overview)

@router.get("/meetings/{id}/topics", response_model=List[TopicResponse])
def get_topics(id: int, service: SummaryService = Depends(get_summary_service)):
    return service.get_topics(id)

@router.post("/meetings/{id}/topics", response_model=TopicResponse, status_code=status.HTTP_201_CREATED)
def create_topic(
    id: int, 
    data: TopicCreate, 
    service: SummaryService = Depends(get_summary_service)
):
    return service.create_topic(id, data.model_dump())

@router.patch("/topics/{id}", response_model=TopicResponse)
def update_topic(
    id: int, 
    data: TopicUpdate, 
    service: SummaryService = Depends(get_summary_service)
):
    return service.update_topic(id, data.model_dump(exclude_unset=True))

@router.delete("/topics/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_topic(id: int, service: SummaryService = Depends(get_summary_service)):
    service.delete_topic(id)
