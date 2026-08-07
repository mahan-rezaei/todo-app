from fastapi import APIRouter, HTTPException, status
from schemas.users import UserCreate, UserRead, UserLogin, UserVerify
from dependecies import SessionDep
from models.users import User, OTP
from sqlmodel import select
from core.security import Hasher
from core.jwt_auth import sign_jwt
from services.smtp import send_email
from fastapi.background import BackgroundTasks


router = APIRouter(prefix="/users")


@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserRead)
async def register_user(user: UserCreate, session: SessionDep, background_tasks: BackgroundTasks):
    user_exists = await session.exec(select(User).where(User.email == user.email))
    if user_exists.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="user with this credential already exists.")
    hashed_password = Hasher.get_hashed_password(user.password)
    user_instance = User.model_validate(user, update={'password': hashed_password})
    session.add(user_instance)
    await session.commit()
    await session.refresh(user_instance)
    otp = OTP.generate(user_instance.email)
    session.add(otp)
    await session.commit()
    await session.refresh(otp)
    background_tasks.add_task(send_email, user_instance.email, otp.code)
    return user_instance


@router.post('/verify', status_code=status.HTTP_200_OK)
async def verify_user(code: UserVerify, session: SessionDep):
    pass


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(user: UserLogin, session: SessionDep):
    user_instance = await session.exec(select(User).where(User.email == user.email))
    user_instance = user_instance.first()
    if not user_instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="user with this email does not exist.")
    if Hasher.verify_passwrod(user.password, user_instance.password):
        token = sign_jwt(user_instance.email, user_instance.id)
        return token
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="password incorrect.")