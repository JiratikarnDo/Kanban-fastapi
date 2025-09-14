from sqlalchemy.orm import Session
from . import models, schemas

# Get User by Email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Create User
def create_user(db: Session, email: str, password_hash: str):
    db_user = models.User(email=email, password_hash=password_hash)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Create Board
def create_board(db: Session, title: str, owner_id: int):
    board = models.Board(title=title, owner_id=owner_id)
    db.add(board)
    db.commit()
    db.refresh(board)
    return board

# Update Board
def update_board(db: Session, board_id: int, title: str):
    board = db.query(models.Board).filter(models.Board.board_id == board_id).first()
    if board:
        board.title = title
        db.commit()
        db.refresh(board)
    return board

# Delete Board
def delete_board(db: Session, board_id: int):
    board = db.query(models.Board).filter(models.Board.board_id == board_id).first()
    if board:
        db.delete(board)
        db.commit()
        return True
    return False

# Add Member to Board
def add_member_to_board(db: Session, board_id: int, user_id: int, role: str):
    existing = db.query(models.BoardMember).filter_by(
        board_id=board_id, user_id=user_id
    ).first()
    if existing:
        return None 
    new_member = models.BoardMember(board_id=board_id, user_id=user_id, role=role)
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member

# Create Task
def create_task(db: Session, task_data: schemas.TaskCreate, current_user: models.User):
    column = db.query(models.BoardColumn).filter(models.BoardColumn.column_id == task_data.column_id).first()
    if not column:
        return None
    task = models.Task(
        title=task_data.title,
        description=task_data.description,
        board_id=column.board_id,
        column_id=task_data.column_id,
        user_id=current_user.user_id,
        due_date=task_data.due_date,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

# Update Task
def update_task(db: Session, task_id: int, title: str = None, description: str = None, status: str = None, position: int = None, due_date: str = None):
    task = db.query(models.Task).filter(models.Task.task_id == task_id).first()
    if not task:
        return None
    if title:
        task.title = title
    if description:
        task.description = description
    if status:
        task.status = status
    if position is not None:
        task.position = position
    if due_date:
        task.due_date = due_date
    db.commit()
    db.refresh(task)
    return task

# Delete Task
def delete_task(db: Session, task_id: int):
    task = db.query(models.Task).filter(models.Task.task_id == task_id).first()
    if not task:
        return False
    db.delete(task)
    db.commit()
    return True

# Get Board Member
def get_board_member(db: Session, board_id: int, user_id: int):
    return db.query(models.BoardMember).filter_by(board_id=board_id, user_id=user_id).first()

# Get Board Members
def get_board_members(db: Session, board_id: int):
    return db.query(models.BoardMember).filter_by(board_id=board_id).all()

# Get Board by ID
def get_board_by_id(db: Session, board_id: int):
    return db.query(models.Board).filter(models.Board.board_id == board_id).first()

# Get Columns by Board
def get_columns_by_board(db: Session, board_id: int):
    return db.query(models.BoardColumn).filter(models.BoardColumn.board_id == board_id).all()

# Get Tasks by Board
def get_tasks_by_board(db: Session, board_id: int):
    return db.query(models.Task).filter(models.Task.board_id == board_id).all()

