from models.users import User, OTP
from dependecies import SessionDep
from sqlmodel import select


async def verify_otp(email, code, session: SessionDep):
    otp_instance = await session.exec(select(OTP).where(OTP.email==email, OTP.code==code))
    otp_instance = otp_instance.first()
    if not otp_instance:
        return False
    if otp_instance.is_expired():
        return False
    return True
