from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=128)
    description: str | None = Field(default=None, nullable=True)
    deadline: datetime

    user: "User" = Relationship(back_populates="tasks", sa_relationship_kwargs={"lazy": "selectin"})
    user_id: int = Field(foreign_key="user.id", ondelete="CASCADE")

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
