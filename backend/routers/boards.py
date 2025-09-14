from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import database, schemas, models
from ..utils.auth_jwt import get_current_user
from backend.service import board_service
from typing import List


router = APIRouter(tags=["Boards"])

# Create Board
@router.post("/", response_model=schemas.BoardResponse)
def create_board(board: schemas.BoardCreate,
                 db: Session = Depends(database.get_db),
                 current_user: models.User = Depends(get_current_user)):
    return board_service.create_board(db, board.title, current_user.user_id)


# Update Board
@router.put("/{board_id}", response_model=schemas.BoardResponse)
def update_board(board_id: int, board: schemas.BoardUpdate,
                 db: Session = Depends(database.get_db),
                 current_user: models.User = Depends(get_current_user)):
    updated = board_service.update_board(db, board_id, board.title)
    if not updated:
        raise HTTPException(status_code=404, detail="Board not found")
    return updated


# Delete Board
@router.delete("/{board_id}")
def delete_board(board_id: int,
                 db: Session = Depends(database.get_db),
                 current_user: models.User = Depends(get_current_user)):
    deleted = board_service.delete_board(db, board_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Board not found")
    return {"detail": "Board deleted"}


# Add Member to Board
@router.post("/{board_id}/invite")
def invite_user(board_id: int, invite: schemas.BoardInvite,
                db: Session = Depends(database.get_db),
                current_user: models.User = Depends(get_current_user)):

    member = board_service.invite_user_to_board(db, board_id, invite.user_id, invite.role)
    if not member:
        raise HTTPException(status_code=400, detail="User already in this board")
    return member

# Get All Boards for Current User
@router.get("/me", response_model=List[schemas.Board])
def get_boards(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    boards = board_service.get_boards(db, current_user)

    return boards

# Get Single Board
@router.get("/{board_id}")
def get_board(
    board_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    return board_service.get_board(db, board_id, current_user)
