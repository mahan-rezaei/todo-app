from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType


SMTP_PASSWORD = "mnvpyqngdzixqltc"
conf = ConnectionConfig(
    MAIL_USERNAME ="mahanrezaei859@gmail.com",
    MAIL_PASSWORD = "mnvpyqngdzixqltc",
    MAIL_FROM = "mahanrezaei859@gmail.com",
    MAIL_PORT = 465,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)
fm = FastMail(conf)

async def send_email(email, otp):
    msg = f"""<b> thanks for your registration.</br>this is your code: {otp}</b>"""
    try:
        message = MessageSchema(subject="Todo OTP code", body=msg, recipients=[email], subtype=MessageType.html)
        await fm.send_message(message)
        print(f"email sent to {email}")
        return True
    except:
        print("faild to sent email.")
        return False
