from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import database, schemas, models
from backend.utils.auth_jwt import get_current_user
from backend.service import task_service
from typing import List


router = APIRouter(tags=["Tasks"])

@router.post("/", response_model=schemas.TaskResponse)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    return task_service.create_task(db, task, current_user)

@router.put("/{task_id}", response_model=schemas.TaskResponse)
def update_task(
    task_id: int,
    task: schemas.TaskUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    updated = task_service.update_task(db, task_id, task, current_user)
    return updated

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    deleted = task_service.delete_task(db, task_id, current_user)
    return deleted

@router.post("/{task_id}/assign", response_model=schemas.TaskAssignee)
def assign_task(
    task_id: int,
    user_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    return task_service.assign_task(db, task_id, user_id, current_user)

@router.get("/me/assignees", response_model=List[schemas.TaskAssignee])
def get_my_assignees(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    return task_service.get_my_assigned_tasks(db, current_user)

@router.get("/{task_id}/assignees", response_model=List[schemas.TaskAssignee])
def get_assignees(
    task_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    return task_service.get_task_assignees(db, task_id, current_user)


