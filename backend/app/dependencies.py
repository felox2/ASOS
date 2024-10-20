import uuid
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine
from sqlmodel import Session

from .config import settings
from .models.users import UserTokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": settings.DB_DRIVER != "sqlite"},
)

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_session():
    with Session(engine) as session:
        yield session


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        user_uid: str = payload.get("sub")

        if user_uid is None:
            raise credentials_exception

        # TODO: check db if user actually exists?
        return UserTokenData(
            uid=uuid.UUID(user_uid),
            email=payload.get("email"),
            name=payload.get("name"),
        )
    except jwt.InvalidTokenError:
        raise credentials_exception


DbSession = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[UserTokenData, Depends(get_current_user)]
