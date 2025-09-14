from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend import database, schemas, models
from backend.utils.auth_jwt import get_current_user
from backend.service import column_service
from typing import List


router = APIRouter(tags=["Columns"])

@router.post("/{board_id}", response_model=schemas.ColumnResponse)
def create_column(board_id: int,
                  column: schemas.ColumnCreate,
                  db: Session = Depends(database.get_db),
                  current_user: models.User = Depends(get_current_user)):
    return column_service.create_column(db, board_id, column.title)

@router.put("/{column_id}", response_model=schemas.ColumnResponse)
def update_column(column_id: int, column: schemas.ColumnUpdate,
                  db: Session = Depends(database.get_db),
                  current_user: models.User = Depends(get_current_user)):
    updated = column_service.update_column(db, column_id, column.title, column.position)
    if not updated:
        raise HTTPException(status_code=404, detail="Column not found")
    return updated

@router.delete("/{column_id}")
def delete_column(column_id: int,
                  db: Session = Depends(database.get_db),
                  current_user: models.User = Depends(get_current_user)):
    deleted = column_service.delete_column(db, column_id, current_user.user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Column not found")
    
    if deleted is False:
        raise HTTPException(status_code=403, detail="Not authorized to delete this column")
    
    return {"detail": "Column deleted"}

@router.get("/{column_id}", response_model=List[schemas.Task])
def get_tasks_by_column(
    column_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    column = db.query(models.BoardColumn).filter(models.BoardColumn.column_id == column_id).first()
    if not column:
        raise HTTPException(status_code=404, detail="Column not found")

    member = (
        db.query(models.BoardMember)
        .filter(models.BoardMember.board_id == column.board_id, models.BoardMember.user_id == current_user.user_id)
        .first()
    )
    if not member:
        raise HTTPException(status_code=403, detail="Not authorized to access this board")

    tasks = db.query(models.Task).filter(models.Task.column_id == column_id).all()
    return tasks