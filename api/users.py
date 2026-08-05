from fastapi import APIRouter, HTTPException, status
from schemas.users import UserCreate
from dependecies import SessionDep
from models.users import User
from sqlmodel import select
from core.security import Hasher
from core.jwt_auth import sign_jwt


router = APIRouter(prefix="/users")


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, session: SessionDep):
    user_exists = await session.exec(select(User).where(User.email == user.email))
    if user_exists.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="user with this credential already exists.")
    hashed_password = Hasher.get_hashed_password(user.password)
    user_instance = User.model_validate(user, update={'password': hashed_password})
    session.add(user_instance)
    await session.commit()
    await session.refresh(user_instance)
    token = sign_jwt(user_instance.email, user_instance.id)
    return token


async def login_user():
    pass