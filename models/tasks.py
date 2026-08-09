from sqlmodel import SQLModel


class Task(SQLModel, table=True):
    pass