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

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserTokenData:
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

class UserOrSession:
    def __init__(self, user: Union[UserTokenData, None] = None, session_id: Union[str, None] = None):
        self.user = user
        self.session_id = session_id


async def get_current_user_or_session(
    request: Request, db: Session = Depends(get_session)
) -> UserOrSession:
    token = request.headers.get("Authorization")
    if token:
        try:
            token = token.split(" ")[1]  
            user = await get_current_user(token)
            return UserOrSession(user=user)
        except Exception:
            pass 

    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
        request.state.session_id = session_id
    else:
        request.state.session_id = session_id

    return UserOrSession(session_id=session_id)

DbSession = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[UserTokenData, Depends(get_current_user)]
CurrentUserOrSession = Annotated[UserOrSession, Depends(get_current_user_or_session)]