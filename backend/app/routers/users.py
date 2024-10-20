from fastapi import APIRouter
from sqlmodel import select

from ..dependencies import CurrentUser, DbSession
from ..models.users import User, UserPublic

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserPublic)
async def read_user_me(db: DbSession, user_current: CurrentUser):
    user = db.exec(select(User).where(User.uid == user_current.uid).limit(1)).first()

    return UserPublic(
        uid=str(user.uid),
        email=user.email,
        name=user.name,
    )
