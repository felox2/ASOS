from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlmodel import Session

from .config import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": settings.DB_DRIVER != "sqlite"},
)


def get_session():
    with Session(engine) as session:
        yield session


DbSession = Annotated[Session, Depends(get_session)]
