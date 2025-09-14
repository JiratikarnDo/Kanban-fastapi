from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from backend import models, schemas


def create_task(db: Session, task_data: schemas.TaskCreate, current_user: models.User):
    new_task = models.Task(
        title=task_data.title,
        description=task_data.description,
        board_id=task_data.board_id,
        column_id=task_data.column_id,
        user_id=current_user.user_id,
        due_date=task_data.due_date,
        status=task_data.status,
        position=task_data.position,
        tags=task_data.tags
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def update_task(db: Session, task_id: int, task_data: schemas.TaskUpdate, current_user: models.User):
    task = db.query(models.Task).filter(models.Task.task_id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    board = db.query(models.Board).filter(models.Board.board_id == task.board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")

    if task.user_id != current_user.user_id and board.owner_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this task"
        )
    task.title = task_data.title
    task.description = task_data.description
    task.due_date = task_data.due_date
    task.status = task_data.status

    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int, current_user: models.User):
    task = db.query(models.Task).filter(models.Task.task_id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    board = db.query(models.Board).filter(models.Board.board_id == task.board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")

    if task.user_id != current_user.user_id and board.owner_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this task"
        )

    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}


def assign_task(db: Session, task_id: int, user_id: int, current_user: models.User):
    task = db.query(models.Task).filter(models.Task.task_id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    board = db.query(models.Board).filter(models.Board.board_id == task.board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")

    if current_user.user_id != board.owner_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to assign this task"
        )
    existing = (
        db.query(models.TaskAssignee)
        .filter(
            models.TaskAssignee.task_id == task_id,
            models.TaskAssignee.user_id == user_id
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=400,
            detail="This user is already assigned to the task"
        )

    task_assignee = models.TaskAssignee(
        task_id=task_id,
        user_id=user_id,
    )
    db.add(task_assignee)
    db.commit()
    db.refresh(task_assignee)
    return task_assignee

def get_task_assignees(db: Session, task_id: int, current_user: models.User):
    task = db.query(models.Task).filter(models.Task.task_id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    board = db.query(models.Board).filter(models.Board.board_id == task.board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")

    member = db.query(models.BoardMember).filter_by(
        board_id=board.board_id,
        user_id=current_user.user_id
    ).first()

    if (
        board.owner_id != current_user.user_id
        and (not member or member.role != "admin")
    ):
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to view assignees"
        )

    return db.query(models.TaskAssignee).filter_by(task_id=task_id).all()

def get_my_assigned_tasks(db: Session, current_user: models.User):
    return (
        db.query(models.TaskAssignee)
        .join(models.Task, models.Task.task_id == models.TaskAssignee.task_id)
        .filter(models.TaskAssignee.user_id == current_user.user_id)
        .all()
    )