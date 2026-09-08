from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional

from app.schemas.action_item import ActionItemResponse, ActionItemCreate, ActionItemUpdate
from app.services.action_item_service import ActionItemService
from app.core.dependencies import get_action_item_service

router = APIRouter(tags=["action_items"])

@router.get("/meetings/{id}/action-items", response_model=List[ActionItemResponse])
def list_action_items(
    id: int, 
    completed: Optional[bool] = None,
    service: ActionItemService = Depends(get_action_item_service)
):
    return service.list_items(id, completed)

@router.post("/meetings/{id}/action-items", response_model=ActionItemResponse, status_code=status.HTTP_201_CREATED)
def create_action_item(
    id: int, 
    data: ActionItemCreate, 
    service: ActionItemService = Depends(get_action_item_service)
):
    return service.create_item(id, data.model_dump(exclude_unset=True))

@router.patch("/action-items/{id}", response_model=ActionItemResponse)
def update_action_item(
    id: int, 
    data: ActionItemUpdate, 
    service: ActionItemService = Depends(get_action_item_service)
):
    return service.update_item(id, data.model_dump(exclude_unset=True))

@router.delete("/action-items/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_action_item(id: int, service: ActionItemService = Depends(get_action_item_service)):
    service.delete_item(id)
