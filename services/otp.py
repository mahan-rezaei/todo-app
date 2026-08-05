from models.users import User, OTP
from dependecies import SessionDep
from sqlmodel import select, desc


async def verify_otp(email, code, session: SessionDep):
    otp_instance = await session.exec(select(OTP).where(OTP.email==email, OTP.code==code, OTP.is_used==False).order_by(desc(OTP.created_at)))
    otp_instance = otp_instance.first()
    if not otp_instance:
        return False
    if otp_instance.is_expired():
        return False
    return True
