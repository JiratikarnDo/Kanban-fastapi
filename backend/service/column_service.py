from sqlalchemy.orm import Session
from backend import models, schemas

def create_column(db: Session, board_id: int, column_title: str):
    new_column = models.BoardColumn(title=column_title, board_id=board_id)
    db.add(new_column)
    db.commit()
    db.refresh(new_column)
    return new_column

def update_column(db: Session, column_id: int, title: str = None, position: int = None):
    column = db.query(models.BoardColumn).filter(models.BoardColumn.column_id == column_id).first()
    if not column:
        return None
    if title:
        column.title = title
    if position is not None:
        column.position = position
    db.commit()
    db.refresh(column)
    return column

def delete_column(db: Session, column_id: int, current_user_id: int):
    column = db.query(models.Column).filter(models.Column.column_id == column_id).first()
    if not column:
        return None
    
    board = db.query(models.Board).filter(models.Board.board_id == column.board_id).first()
    if not board:
        return False

    if board.owner_id != current_user_id:
        return False

    db.delete(column)
    db.commit()
    return True