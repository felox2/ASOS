from fastapi import  HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlmodel import Session, select
from ..config import settings
from ..models.users import User
from ..dependencies import DbSession
import uuid

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(db: DbSession, token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = db.exec(select(User).where(User.uid == uuid.UUID(user_id))).first()
    if user is None:
        raise credentials_exception
    return user

def admin_required(current_user: User = get_current_user):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
    return current_user