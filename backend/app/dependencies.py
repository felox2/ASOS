import uuid
from typing import Annotated, Union


from fastapi import Depends, HTTPException, Request
from sqlmodel import Session

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine
from sqlmodel import Session

from .config import settings
from .models.users import UserTokenData, User

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


async def get_current_user_or_session(
    request: Request, db: Session = Depends(get_session)
) -> Union[UserTokenData, str]:
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
        request.state.session_id = session_id
    else:
        request.state.session_id = session_id

    user = None
    if "user_id" in request.cookies:
        user_id = request.cookies["user_id"]
        user = db.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
    return user or session_id

DbSession = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[UserTokenData, Depends(get_current_user)]
CurrentUserOrSession = Annotated[Union[UserTokenData, str], Depends(get_current_user_or_session)]
