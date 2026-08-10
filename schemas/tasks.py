from pydantic import BaseModel
from datetime import datetime
from schemas.users import UserRead


class TaskBase(BaseModel):
    title: str
    description: str
    deadline: datetime


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int
    user: UserRead
    created_at: datetime
    updated_at: datetime