from sqlmodel import SQLModel, Field
from datetime import datetime, UTC


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    full_name: str = Field(max_length=68)
    email: str = Field(unique=True, index=True)
    age: int | None = Field(default=None)
    password: str

    created_at: datetime = Field(default_factory=datetime.now(UTC))
    updated_at: datetime = Field(default_factory=datetime.now(UTC))