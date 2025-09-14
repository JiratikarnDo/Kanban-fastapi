from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import List, Optional

# User
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str

class UserResponse(UserBase):
    user_id: int
    status: str

    class Config:
        orm_mode = True

# Token
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Board
class BoardBase(BaseModel):
    title: str

class BoardCreate(BoardBase):
    pass

class BoardUpdate(BoardBase):
    pass

class BoardResponse(BoardBase):
    board_id: int
    owner_id: int

    class Config:
        orm_mode = True

# Board Member
class BoardMemberBase(BaseModel):
    user_id: int

class BoardMemberCreate(BoardMemberBase):
    role: Optional[str] = "member"

class BoardMemberResponse(BoardMemberBase):
    id: int
    board_id: int
    role: str

    class Config:
        from_attributes = True

# Board Invite
class BoardInvite(BaseModel):
    user_id: int
    role: str

class ColumnBase(BaseModel):
    title: str

class ColumnCreate(ColumnBase):
    pass

class ColumnUpdate(BaseModel):
    title: Optional[str] = None
    position: Optional[int] = None

# Column Response
class ColumnResponse(ColumnBase):
    column_id: int
    board_id: int
    position: int

    class Config:
        from_attributes = True

# Task
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    board_id: int
    column_id: int
    due_date: Optional[datetime] = None
    status: str = "To Do"
    position: int = 0
    tags: List[str] = []

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    position: Optional[int] = None
    due_date: Optional[datetime] = None

class TaskResponse(BaseModel):
    task_id: int
    title: str
    description: Optional[str]
    board_id: int
    column_id: int
    user_id: int
    due_date: Optional[datetime]
    status: str
    position: int
    created_at: datetime

    class Config:
        from_attributes = True

class TaskAssigneeBase(BaseModel):
    task_id: int
    user_id: int

class TaskAssignee(TaskAssigneeBase):
    assigned_at: datetime

    class Config:
        from_attributes = True 

class Board(BaseModel):
    board_id: int
    title: str
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class BoardColumn(BaseModel):
    column_id: int
    title: str
    board_id: int
    position: int
    created_at: datetime

    class Config:
        from_attributes = True


class Task(BaseModel):
    task_id: int
    title: str
    description: Optional[str]
    board_id: int
    column_id: int
    user_id: int
    due_date: Optional[datetime]
    status: str
    position: int
    created_at: datetime
    tags: List[str] = []

    class Config:
        from_attributes = True

class ColumnOut(BaseModel):
    id: int
    name: str
    order: int
    model_config = ConfigDict(from_attributes=True)  