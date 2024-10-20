import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlmodel import select

from ..config import settings
from ..dependencies import DbSession
from ..models.users import Session, User, UserCreate, UserPublic

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
invalid_credentials = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)
invalid_session = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid session",
    headers={"WWW-Authenticate": "Bearer"},
)


class TokenResponse(BaseModel):
    access_token: str


def get_access_token(user: User):
    return jwt.encode(
        {
            "sub": str(user.uid),
            "email": user.email,
            "name": user.name,
            # TODO: make configurable?
            "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
        },
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


@router.post("/register", response_model=UserPublic)
async def register(db: DbSession, input: UserCreate):
    stmt = select(User).where(User.email == input.email).limit(1)
    result = db.exec(stmt).first()

    if result is not None:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, "user with this email already exists"
        )

    user = User(
        uid=uuid.uuid4(),
        email=input.email,
        name=input.name,
        password_hash=pwd_context.hash(input.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.post("/login", response_model=TokenResponse)
async def login(
    response: Response,
    db: DbSession,
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = db.exec(select(User).where(User.email == data.username).limit(1)).first()

    if user is None:
        raise invalid_credentials
    if not pwd_context.verify(data.password, user.password_hash):
        raise invalid_credentials

    session = Session(
        refresh_token=secrets.token_urlsafe(64),
        user=user,
        # TODO: make configurable?
        expires_at=datetime.now(timezone.utc) + timedelta(days=30),
    )

    access_token = get_access_token(user)

    response.set_cookie(
        key="refresh_token",
        value=session.refresh_token,
        expires=session.expires_at,
        httponly=True,
        samesite="strict",
    )

    db.add(session)
    db.commit()

    return TokenResponse(access_token=access_token)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(db: DbSession, refresh_token: Annotated[str, Cookie()]):
    session = db.exec(
        select(Session).where(Session.refresh_token == refresh_token).limit(1)
    ).first()

    now = datetime.now(timezone.utc)

    if session is None:
        raise invalid_session
    if session.expires_at.replace(tzinfo=timezone.utc) < now:
        raise invalid_session

    return TokenResponse(access_token=get_access_token(session.user))


@router.post("/logout")
async def logout(
    response: Response, db: DbSession, refresh_token: Annotated[str, Cookie()]
):
    # TODO: also invalidate jwt?

    session = db.exec(
        select(Session).where(Session.refresh_token == refresh_token).limit(1)
    ).first()

    now = datetime.now(timezone.utc)

    if session is None:
        raise invalid_session
    if session.expires_at.replace(tzinfo=timezone.utc) < now:
        raise invalid_session

    session.expires_at = now

    db.add(session)
    db.commit()

    response.delete_cookie(key="refresh_token")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
