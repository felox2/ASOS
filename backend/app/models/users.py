from datetime import datetime
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    email: str = Field(unique=True)
    name: str = Field()
    password_hash: str = Field()

    created_at: datetime = Field(default=datetime.now())
    modified_at: datetime = Field(default=datetime.now())
