from sqlmodel import SQLModel, Field
from datetime import datetime, UTC, timedelta
import string
import secrets


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    full_name: str = Field(max_length=68)
    email: str = Field(unique=True, index=True)
    age: int | None = Field(default=None)
    password: str

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class OTP(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str
    code: str
    expires_at: datetime
    is_used: bool = False

    @classmethod
    def generate(cls, email: str, length=4):
        digits = string.digits
        code = ''.join(secrets.choice(digits) for _ in range(length))

        return cls(email=email, code=code, expires_at=datetime.now() + timedelta(minutes=5))

    def is_expired(self):
        return datetime.now() > self.expires_at

