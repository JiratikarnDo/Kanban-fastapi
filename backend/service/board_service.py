from http.client import HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from .. import models

def create_board(db: Session, title: str, owner_id: int):
    return crud.create_board(db, title, owner_id)


def update_board(db: Session, board_id: int, new_title: str):
    return crud.update_board(db, board_id, new_title)


def delete_board(db: Session, board_id: int):
    return crud.delete_board(db, board_id)


def invite_user_to_board(db: Session, board_id: int, user_id: int, role: str):
    return crud.add_member_to_board(db, board_id, user_id, role)


def get_boards(db: Session, current_user: models.User):
    return (
        db.query(models.Board)
        .join(models.BoardMember, models.Board.board_id == models.BoardMember.board_id)
        .filter(models.BoardMember.user_id == current_user.user_id)
        .all()
    )

def get_board(db: Session, board_id: int, current_user: models.User):
    board = crud.get_board_by_id(db, board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")

    is_owner = board.owner_id == current_user.user_id
    is_member = crud.get_board_member(db, board_id, current_user.user_id)

    if not (is_owner or is_member):
        raise HTTPException(status_code=403, detail="Access denied")

    columns = crud.get_columns_by_board(db, board_id)
    tasks = crud.get_tasks_by_board(db, board_id)
    members = crud.get_board_members(db, board_id)

    return {
        "board_id": board.board_id,
        "title": board.title,
        "owner_id": board.owner_id,
        "created_at": board.created_at,
        "columns": columns,
        "tasks": tasks,
        "members": members,
    }
