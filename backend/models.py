from sqlalchemy import JSON, Column, String, BigInteger, TIMESTAMP, Text, func
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Integer, ForeignKey

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    status = Column(String(20), default="active")
    created_at = Column(TIMESTAMP, server_default=func.now())

    tasks = relationship("Task", back_populates="user")
    assigned_tasks = relationship("TaskAssignee", back_populates="user")


class Board(Base):
    __tablename__ = "boards"

    board_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.user_id"))
    created_at = Column(TIMESTAMP, server_default=func.now())

    owner = relationship("User")
    tasks = relationship("Task", back_populates="board")
    columns = relationship("BoardColumn", back_populates="board")


class BoardMember(Base):
    __tablename__ = "board_members"

    board_id = Column(Integer, ForeignKey("boards.board_id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    role = Column(String(50))
    joined_at = Column(TIMESTAMP, server_default=func.now())

    board = relationship("Board", backref="members")
    user = relationship("User", backref="boards")

class BoardColumn(Base):
    __tablename__ = "columns"

    column_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    board_id = Column(Integer, ForeignKey("boards.board_id"), nullable=False)
    position = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())

    board = relationship("Board", back_populates="columns")
    tasks = relationship("Task", back_populates="column")


class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    board_id = Column(Integer, ForeignKey("boards.board_id"))
    column_id = Column(Integer, ForeignKey("columns.column_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    due_date = Column(TIMESTAMP, nullable=True)
    status = Column(String(50), default="To Do")
    position = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())

    board = relationship("Board", back_populates="tasks")
    column = relationship("BoardColumn", back_populates="tasks")
    user = relationship("User", back_populates="tasks")
    assignees = relationship("TaskAssignee", back_populates="task")
    tags = Column(JSON, nullable=True, default=[])



class TaskAssignee(Base):
    __tablename__ = "task_assignees"

    task_id = Column(Integer, ForeignKey("tasks.task_id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    assigned_at = Column(TIMESTAMP, server_default=func.now())

    task = relationship("Task", back_populates="assignees")
    user = relationship("User", back_populates="assigned_tasks")
