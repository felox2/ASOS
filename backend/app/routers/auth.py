from fastapi import APIRouter
from sqlmodel import select

from app.dependencies import DbSession
from app.models.users import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def read_user_me(db: DbSession):
    users = db.exec(select(User).limit(2)).all()

    print(users)

    return {"username": "test"}
